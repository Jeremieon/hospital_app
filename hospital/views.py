from rest_framework import viewsets, permissions
from django.http import HttpResponse
from django.conf import settings
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import MyTokenObtainPairSerializer
from django.http import JsonResponse
from django.conf import settings
from hospital_mgt.utils import load_public_key_components
from .models import Patient, Doctor, Prescription, Note
from .permissions import IsDoctor
from .serializers import (
    PatientSerializer,
    DoctorSerializer,
    PrescriptionSerializer,
    NoteSerializer,
    MyTokenObtainPairSerializer,
)


class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [permissions.IsAuthenticated, IsDoctor]


class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [permissions.IsAuthenticated]


class PrescriptionViewSet(viewsets.ModelViewSet):
    queryset = Prescription.objects.all()
    serializer_class = PrescriptionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        doctor = self.request.user.doctor
        serializer.save(doctor=doctor)


class NoteViewSet(viewsets.ModelViewSet):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = [permissions.IsAuthenticated]


def public_key_view(request):
    return HttpResponse(settings.SIMPLE_JWT["VERIFYING_KEY"], content_type="text/plain")


def jwks_view(request):
    public_key = settings.SIMPLE_JWT["VERIFYING_KEY"]
    jwk = load_public_key_components(public_key)
    return JsonResponse({"keys": [jwk]})


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
