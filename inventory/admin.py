from django.contrib import admin
from .models import Medicine, Sale, Inventory, Category


# Register your models here.
admin.register(Medicine)


class MedicineAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "stock", "price_per_unit", "created_at")
    readonly_fields = "stock"


admin.register(Inventory)
admin.site.register(Sale)
admin.site.register(Category)
