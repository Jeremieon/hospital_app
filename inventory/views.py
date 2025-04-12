from rest_framework import viewsets, generics, permissions
from .models import Medicine, Sale, Inventory, User, Category
from django.db.models import F
from rest_framework_simplejwt.tokens import RefreshToken
from django.db.models.functions import Cast
from hospital.permissions import IsDoctor
from rest_framework import serializers
from .serializers import (
    MedicineSerializer,
    SaleSerializer,
    InventorySerializer,
    CategorySerializer,
    UserSerializer,
)
from rest_framework.permissions import IsAuthenticated
from .serializers import UserProfileSerializer
from rest_framework.response import Response
from datetime import date
from django.db.models import Sum
from rest_framework.views import APIView


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]


class MedicineViewSet(viewsets.ModelViewSet):
    queryset = Medicine.objects.all()
    serializer_class = MedicineSerializer
    permission_classes = [IsAuthenticated]


class SaleViewSet(viewsets.ModelViewSet):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer
    permission_classes = [IsAuthenticated, IsDoctor]


class InventoryViewSet(viewsets.ModelViewSet):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer
    permission_classes = [IsAuthenticated]


class RegisterUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        user = response.data
        refresh = RefreshToken.for_user(User.objects.get(username=user["username"]))
        user["refresh"] = str(refresh)
        user["access"] = str(refresh.access_token)
        return Response(user, status=status.HTTP_201_CREATED)


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        data = {
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
        }
        return Response(data)


class DailySalesAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        today = date.today()

        # Annotate the total sale amount based on quantity_sold and price_per_unit
        daily_sales = (
            Sale.objects.filter(sale_date__date=today, sold_by=request.user)
            .annotate(
                total_sale_amount=F("quantity_sold") * F("medicine__price_per_unit")
            )
            .aggregate(total_sales=Sum("total_sale_amount"))
        )

        total_sales = daily_sales["total_sales"] or 0  # Default to 0 if no sales

        return Response(
            {
                "date": today.strftime("%Y-%m-%d"),
                "total_sales": total_sales,
            }
        )
