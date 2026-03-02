from django.db import models
from core.models import User


class Department(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Hospital(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='hospital_profile')
    name = models.CharField(max_length=200)
    address = models.TextField()
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100, default='Bangladesh')
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    website = models.URLField(blank=True)
    description = models.TextField(blank=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='doctor_profile')
    hospital = models.ForeignKey(Hospital, on_delete=models.SET_NULL, null=True, blank=True, related_name='doctors')
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    specialization = models.CharField(max_length=100)
    qualification = models.CharField(max_length=200)
    experience_years = models.PositiveIntegerField(default=0)
    consultation_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    available_days = models.CharField(max_length=200, default='Monday,Tuesday,Wednesday,Thursday,Friday')
    bio = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    address = models.TextField(blank=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Dr. {self.user.get_full_name() or self.user.username} - {self.specialization}"


class DoctorApplication(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('ACCEPTED', 'Accepted'),
        ('REJECTED', 'Rejected'),
    ]
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='applications')
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, related_name='applications')
    cover_letter = models.TextField(blank=True, help_text='Why do you want to join this hospital?')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    response_message = models.TextField(blank=True)
    applied_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('doctor', 'hospital')
        ordering = ['-applied_at']

    def __str__(self):
        return f"{self.doctor} → {self.hospital} [{self.status}]"


class Patient(models.Model):
    BLOOD_GROUP_CHOICES = [
        ('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'),
        ('O+', 'O+'), ('O-', 'O-'), ('AB+', 'AB+'), ('AB-', 'AB-'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='patient_profile')
    date_of_birth = models.DateField(null=True, blank=True)
    blood_group = models.CharField(max_length=5, choices=BLOOD_GROUP_CHOICES, blank=True)
    address = models.TextField(blank=True)
    emergency_contact = models.CharField(max_length=15, blank=True)
    medical_history = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.get_full_name() or self.user.username


class Appointment(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('CONFIRMED', 'Confirmed'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ]
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='appointments')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='appointments')
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    symptoms = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-appointment_date', '-appointment_time']

    def __str__(self):
        return f"{self.patient} -> Dr.{self.doctor} on {self.appointment_date}"


class MedicalRecord(models.Model):
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE, related_name='medical_record')
    diagnosis = models.TextField()
    prescription = models.TextField(blank=True)
    follow_up_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Record for {self.appointment}"
