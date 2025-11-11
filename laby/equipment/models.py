from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = [
        ('Admin', 'Admin'),
        ('Staff', 'Staff'),
        ('Viewer', 'Viewer'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.username} ({self.role})"

class Supplier(models.Model):
    name = models.CharField(max_length=100)
    contact_no = models.CharField(max_length=15)
    email = models.EmailField()
    street = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    pincode = models.CharField(max_length=10)

    def __str__(self):
        return self.name

class Equipment(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, related_name='equipments')
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    condition = models.CharField(max_length=50, blank=True)
    location = models.CharField(max_length=100)
    added_on = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name

class UsageRecord(models.Model):
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, related_name='usage_records')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='usage_records')
    borrowed_on = models.DateField()
    returned_on = models.DateField(null=True, blank=True)
    purpose = models.TextField()
    quantity_used = models.PositiveIntegerField()

class Alert(models.Model):
    ALERT_TYPES = [
        ('low_stock', 'Low Stock'),
        ('maintenance', 'Maintenance'),
    ]
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, related_name='alerts')
    message = models.TextField()
    type = models.CharField(max_length=20, choices=ALERT_TYPES)
    created_at = models.DateField(auto_now_add=True)
