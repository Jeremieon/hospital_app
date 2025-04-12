from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Patient(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    discharge_date = models.DateField(null=True, blank=True)
    date_admitted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    specialization = models.CharField(max_length=100)

    def save(self, *args, **kwargs):
        if not self.user.first_name.startswith("Dr. "):
            self.user.first_name = f"Dr. {self.user.first_name}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Dr. {self.user.username}"


class Prescription(models.Model):
    patient = models.ForeignKey(
        Patient, related_name="prescriptions", on_delete=models.CASCADE
    )
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    comments = models.TextField()
    medicine = models.CharField(max_length=200)
    date_prescribed = models.DateTimeField(auto_now_add=True)
    prescription_issued = models.BooleanField(default=False)

    def __str__(self):
        return f"Prescription for {self.patient.name} by {self.doctor.user.username}"


class Note(models.Model):
    patient = models.ForeignKey(Patient, related_name="notes", on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Note for {self.patient.name}"
