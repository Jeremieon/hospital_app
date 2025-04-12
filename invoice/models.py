from django.db import models
import random


def generate_invoice_number():
    return f"JER-{random.randint(1000000, 9999999)}"


class Invoice(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("paid", "Paid"),
        ("cancelled", "Cancelled"),
    ]

    invoice_number = models.CharField(
        max_length=20, unique=True, default=generate_invoice_number, editable=False
    )
    customer_name = models.CharField(max_length=100)
    customer_name = models.CharField(max_length=100)
    customer_email = models.EmailField()
    issue_date = models.DateField(auto_now_add=True)
    due_date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")

    def __str__(self):
        return f"Invoice {self.invoice_number} - {self.customer_name}"

    @property
    def total_amount(self):
        return sum(
            item.total_price for item in self.items.all()
        )  # Sum of all item prices


class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, related_name="items", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.name} ({self.quantity}x)"

    @property
    def total_price(self):
        return self.quantity * self.unit_price  # Total price per item
