from django.contrib.auth import authenticate
from rest_framework import status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from .serializers import (
    UserRegistrationSerializer,
    UserLoginSerializer,
    ProductSerializer,
    BillSerializer,
    BillDetailSerializer,
)
from ..models import Product, Bill, BillDetail
from ..permissions import CustomPermission, IsCustomer, IsEmployee


class UserRegistrationLoginViewSet(ViewSet):

    @action(methods=["post"], detail=False)
    def register(self, request):
        serializer = UserRegistrationSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=["post"], detail=False)
    def login(self, request):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get("username")
        password = serializer.validated_data.get("password")
        user = authenticate(request, username=username, password=password)
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response(data={"token": token.key}, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [CustomPermission]


class BillViewSet(viewsets.ModelViewSet):
    queryset = Bill.objects.all()
    serializer_class = BillSerializer
    permission_classes = [IsEmployee]


class BillDetailViewSet(viewsets.ModelViewSet):
    queryset = BillDetail.objects.all()
    serializer_class = BillDetailSerializer
    permission_classes = [IsCustomer]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        bill = serializer.validated_data["bill"]
        product = serializer.validated_data["product"]
        quantity = serializer.validated_data["quantity"]

        existing_details = BillDetail.objects.filter(bill=bill, product=product).first()

        if existing_details:
            existing_details.quantity = quantity
            existing_details.total_cost = product.price * existing_details.quantity
            existing_details.save()
            return Response(
                self.get_serializer(existing_details).data, status=status.HTTP_200_OK
            )
        else:
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(
                serializer.data, status=status.HTTP_201_CREATED, headers=headers
            )

    def perform_create(self, serializer):
        serializer.save()
