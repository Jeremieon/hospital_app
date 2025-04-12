from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.contrib import admin
from hospital.views import public_key_view
from hospital.views import jwks_view
from hospital.views import MyTokenObtainPairView
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)


urlpatterns = [
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("admin/", admin.site.urls),
    path("api/", include("inventory.urls")),
    path("api/hospital/", include("hospital.urls")),
    path("api/invoice/", include("invoice.urls")),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("jwks/", jwks_view, name="jwks"),
    path("public-key/", public_key_view, name="public-key"),
    path("api/token/", MyTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path("api/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
]
