from django.contrib import admin
from .models import Department, Doctor, Patient, Appointment, MedicalRecord, Hospital, DoctorApplication


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Hospital)
class HospitalAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'country', 'user')
    search_fields = ('name', 'city')


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('user', 'specialization', 'department', 'hospital', 'city', 'experience_years', 'is_available')
    list_filter = ('department', 'is_available', 'hospital')
    search_fields = ('user__username', 'user__first_name', 'specialization', 'city')


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('user', 'blood_group', 'date_of_birth')
    search_fields = ('user__username', 'user__first_name')


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'appointment_date', 'appointment_time', 'status')
    list_filter = ('status', 'appointment_date')


@admin.register(MedicalRecord)
class MedicalRecordAdmin(admin.ModelAdmin):
    list_display = ('appointment', 'created_at')


@admin.register(DoctorApplication)
class DoctorApplicationAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'hospital', 'status', 'applied_at', 'reviewed_at')
    list_filter = ('status',)
