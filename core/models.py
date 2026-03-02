from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = (
        ('PATIENT', 'Patient'),
        ('DOCTOR', 'Doctor'),
        ('HOSPITAL', 'Hospital Admin'),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    phone = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return f"{self.username} ({self.role})"
