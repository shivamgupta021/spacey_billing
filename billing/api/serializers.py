from rest_framework import serializers

from billing.models import User, Product, BillDetail, Bill


class UserRegistrationSerializer(serializers.ModelSerializer):
    raw_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("id", "username", "email", "raw_password", "user_type")
        read_only_fields = ("id",)

    def create(self, validated_data):
        if self.context.get("request"):
            request = self.context.get("request")
            if request.user.is_authenticated and request.user.user_type == "employee":
                if validated_data["user_type"] == "customer":
                    user = User.objects.create_user(
                        username=validated_data["username"],
                        email=validated_data["email"],
                        password=validated_data["raw_password"],
                        user_type=validated_data["user_type"],
                    )
                    return user
                else:
                    raise serializers.ValidationError(
                        "Only customers can be created by employees."
                    )
            else:
                user = User.objects.create_user(
                    username=validated_data["username"],
                    email=validated_data["email"],
                    password=validated_data["raw_password"],
                    user_type=validated_data["user_type"],
                )
                return user
        else:
            raise serializers.ValidationError("Request object not found in context.")


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ("id", "name", "price", "quantity_in_stock", "created")
        read_only_fields = ("id", "created")

    def create(self, validated_data):
        product = Product(
            name=validated_data["name"],
            price=validated_data["price"],
            quantity_in_stock=validated_data["quantity_in_stock"],
        )
        product.save()
        return product


class BillDetailSerializer(serializers.ModelSerializer):
    price = serializers.SerializerMethodField()

    class Meta:
        model = BillDetail
        fields = ("id", "bill", "product", "quantity", "price", "total_cost")

    def get_price(self, obj):
        return obj.product.price

    def create(self, validated_data):
        bill = validated_data.pop("bill")
        product = validated_data.pop("product")
        quantity = validated_data.pop("quantity")
        total_cost = product.price * quantity
        bill_detail = BillDetail.objects.create(
            bill=bill, product=product, quantity=quantity, total_cost=total_cost
        )
        return bill_detail


class BillSerializer(serializers.ModelSerializer):
    bill_details = serializers.SerializerMethodField()
    total_amount = serializers.SerializerMethodField()

    class Meta:
        model = Bill
        fields = ("id", "customer", "employee", "total_amount", "bill_details")
        read_only_fields = ("id", "bill_details", "total_amount")

    def get_bill_details(self, obj):
        details = obj.billdetail_set.all()
        return BillDetailSerializer(details, many=True).data

    def get_total_amount(self, obj):
        return sum(detail.total_cost for detail in obj.billdetail_set.all())

    def validate(self, attrs):
        customer = attrs["customer"]
        employee = attrs["employee"]

        if Bill.objects.filter(customer=customer, employee=employee).exists():
            raise serializers.ValidationError(
                "A bill with the same customer and employee already exists."
            )

        return attrs
