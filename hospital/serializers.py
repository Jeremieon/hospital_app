from rest_framework import serializers
from .models import Patient, Doctor, Prescription, Note
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
import uuid
from rest_framework import serializers
from django.contrib.auth.models import Permission


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ["id", "patient", "content", "created_at"]


class PrescriptionSerializer(serializers.ModelSerializer):
    doctor = serializers.SerializerMethodField()

    class Meta:
        model = Prescription
        fields = [
            "id",
            "patient",
            "doctor",
            "comments",
            "medicine",
            "date_prescribed",
            "prescription_issued",
        ]

    def get_doctor(self, obj) -> str:
        return f"Dr. {obj.doctor.user.first_name}"


class PatientSerializer(serializers.ModelSerializer):
    prescriptions = PrescriptionSerializer(many=True, read_only=True)
    notes = NoteSerializer(many=True, read_only=True)

    class Meta:
        model = Patient
        fields = [
            "id",
            "name",
            "age",
            "date_admitted",
            "prescriptions",
            "notes",
            "discharge_date",
        ]


class DailySalesResponseSerializer(serializers.Serializer):
    date = serializers.DateField()
    total_sales = serializers.DecimalField(max_digits=10, decimal_places=2)


class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = "__all__"


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["iss"] = "Jeremieon"
        token["aud"] = user.username
        token["typ"] = "Bearer"
        token["sid"] = str(uuid.uuid4())
        token["acr"] = "1"
        token["email_verified"] = False
        token["sub"] = str(user.id)
        token["name"] = f"{user.first_name} {user.last_name}"
        token["preferred_username"] = user.username
        token["given_name"] = user.first_name
        token["family_name"] = user.last_name
        token["email"] = user.email
        token["roles"] = [group.name for group in user.groups.all()][0]
        return token
