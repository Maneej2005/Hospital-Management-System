from django.db import models

# Create your models here.
from django.contrib.auth.models import User






class Doctor(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE
    )
    specialization = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)

    def __str__(self):
        return self.user.username


class Patient(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE
    )
    age = models.IntegerField()
    gender = models.CharField(max_length=20)
    phone = models.CharField(max_length=15)
    address = models.TextField()

    def __str__(self):
        return self.user.username


class Appointment(models.Model):

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]

    patient = models.ForeignKey(
        Patient, on_delete=models.CASCADE
    )

    doctor = models.ForeignKey(
        Doctor, on_delete=models.CASCADE
    )

    appointment_date = models.DateField()
    reason = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Pending'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient} - {self.doctor}"