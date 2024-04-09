from rest_framework import serializers

from billing.models import Employee, Customer, Product, Bill, BillDetails


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class BillDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BillDetails
        fields = '__all__'


class BillSerializer(serializers.ModelSerializer):
    bill_details = BillDetailsSerializer(many=True, read_only=True)

    class Meta:
        model = Bill
        fields = '__all__'
