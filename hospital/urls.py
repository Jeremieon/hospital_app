from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r"patients", views.PatientViewSet)
router.register(r"doctors", views.DoctorViewSet)
router.register(r"prescriptions", views.PrescriptionViewSet)
router.register(r"notes", views.NoteViewSet)  

urlpatterns = router.urls
