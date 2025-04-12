from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Medicine(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="medicines",
        blank=True,
        null=True,
    )
    description = models.TextField(null=True, blank=True)
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.name

    @property
    def stock(self):
        """Get the total stock from Inventory"""
        inventory = Inventory.objects.filter(medicine=self).first()
        return inventory.quantity_in_stock if inventory else 0


from django.db import models, transaction
from django.core.exceptions import ValidationError


class Sale(models.Model):
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    quantity_sold = models.PositiveIntegerField()
    sold_by = models.ForeignKey(User, on_delete=models.CASCADE)
    sale_date = models.DateTimeField(auto_now_add=True)

    def total_sale_amount(self):
        return self.quantity_sold * self.medicine.price_per_unit

    def save(self, *args, **kwargs):
        """Update inventory stock when a sale is made"""
        with transaction.atomic():
            inventory = Inventory.objects.filter(
                medicine=self.medicine
            ).first()  # Get related inventory

            if inventory is None:
                raise ValidationError(f"No inventory found for {self.medicine.name}")

            if self.pk is None:
                # New sale
                if inventory.quantity_in_stock >= self.quantity_sold:
                    inventory.quantity_in_stock -= self.quantity_sold
                    inventory.save()
                else:
                    raise ValidationError("Insufficient stock to fulfill the order.")
            else:
                # Editing an existing sale
                original_sale = Sale.objects.get(id=self.pk)
                quantity_difference = self.quantity_sold - original_sale.quantity_sold

                if quantity_difference > 0:  # Increase in quantity sold
                    if inventory.quantity_in_stock >= quantity_difference:
                        inventory.quantity_in_stock -= quantity_difference
                    else:
                        raise ValidationError(
                            "Not enough stock to fulfill the updated order."
                        )
                elif quantity_difference < 0:  # Decrease in quantity sold
                    inventory.quantity_in_stock += abs(
                        quantity_difference
                    )  # Re-add the stock

                inventory.save()

            super().save(*args, **kwargs)

    def __str__(self):
        return f"Sale of {self.quantity_sold} {self.medicine.name} by {self.sold_by.username} on {self.sale_date}"


class Inventory(models.Model):
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    quantity_in_stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.medicine.name} - {self.quantity_in_stock} units in stock"

    def update_stock(self, quantity_sold):
        """Update stock after sale"""
        if self.quantity_in_stock >= quantity_sold:
            self.quantity_in_stock -= quantity_sold
            self.save()
        else:
            raise ValueError("Not enough stock to complete the sale")

    def restock(self, quantity):
        if quantity > 0:
            self.quantity_in_stock += quantity
            self.save()
        else:
            raise ValueError("Restock quantity must be positive.")
