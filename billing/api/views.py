from rest_framework import viewsets, permissions

from billing.api.serializers import ProductSerializer
from billing.models import Product


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]
