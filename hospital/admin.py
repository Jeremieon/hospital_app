from django.contrib import admin
from .models import Patient, Doctor, Prescription, Note


admin.site.register(Patient)
admin.site.register(Doctor)
admin.site.register(Prescription)
admin.site.register(Note)
