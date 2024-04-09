from rest_framework import serializers

from billing.models import Product, Bill, BillDetail


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class BillDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = BillDetail
        fields = "__all__"


class BillSerializer(serializers.ModelSerializer):
    bill_details = BillDetailSerializer(many=True, read_only=True)

    class Meta:
        model = Bill
        fields = "__all__"
