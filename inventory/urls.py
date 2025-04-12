from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import DailySalesAPIView, UserProfileView

router = DefaultRouter()
router.register(r"categories", views.CategoryViewSet)
router.register(r"medicines", views.MedicineViewSet)
router.register(r"sales", views.SaleViewSet)
router.register(r"", views.InventoryViewSet)


urlpatterns = [
    path("inventory/", include(router.urls)),
    path("daily-sales/", DailySalesAPIView.as_view(), name="daily-sales"),
    path("profile/", UserProfileView.as_view(), name="user-profile"),
]
