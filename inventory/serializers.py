from rest_framework import serializers
from .models import Medicine, Sale, Inventory, User, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class MedicineSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source="category.name", read_only=True)
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = Medicine
        fields = [
            "id",
            "name",
            "category",
            "description",
            "price_per_unit",
            "stock",
            "created_at",
            "updated_at",
        ]


class SaleSerializer(serializers.ModelSerializer):
    medicine_name = serializers.CharField(source="medicine.name", read_only=True)
    total_sale_amount = serializers.DecimalField(
        read_only=True, max_digits=10, decimal_places=2
    )
    remaining_stock = serializers.SerializerMethodField()
    sold_by = serializers.CharField(source="sold_by.username", read_only=True)

    class Meta:
        model = Sale
        fields = [
            "id",
            "medicine_name",
            "quantity_sold",
            "sold_by",
            "sale_date",
            "total_sale_amount",
            "remaining_stock",
        ]

    def get_remaining_stock(self, obj):
        # Access the medicine associated with the sale and calculate remaining stock
        medicine = obj.medicine
        remaining_stock = (
            medicine.stock - obj.quantity_sold
        )  # Adjust based on your sale model
        return remaining_stock


class InventorySerializer(serializers.ModelSerializer):
    medicine_name = serializers.CharField(source="medicine.name", read_only=True)

    class Meta:
        model = Inventory
        fields = ["id", "medicine_name", "quantity_in_stock"]


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "email", "password", "first_name", "last_name"]

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
            first_name=validated_data.get("first_name", ""),
            last_name=validated_data.get("last_name", ""),
        )
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name"]
