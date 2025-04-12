from rest_framework import serializers
from .models import Invoice, InvoiceItem
from drf_spectacular.utils import extend_schema_field


class InvoiceItemSerializer(serializers.ModelSerializer):
    total_price = serializers.ReadOnlyField()

    class Meta:
        model = InvoiceItem
        fields = ["id", "name", "description", "quantity", "unit_price", "total_price"]


class InvoiceSerializer(serializers.ModelSerializer):
    items = InvoiceItemSerializer(many=True)  # Nesting items inside invoice
    total_amount = serializers.ReadOnlyField()

    class Meta:
        model = Invoice
        fields = [
            "id",
            "invoice_number",
            "customer_name",
            "customer_email",
            "issue_date",
            "due_date",
            "status",
            "items",
            "total_amount",
        ]

    @extend_schema_field(float)
    def get_total_amount(self):
        return self.instance.total_amount

    def create(self, validated_data):
        items_data = validated_data.pop("items")  # Extract items
        invoice = Invoice.objects.create(**validated_data)  # Create invoice
        for item_data in items_data:
            InvoiceItem.objects.create(invoice=invoice, **item_data)  # Add items
        return invoice
