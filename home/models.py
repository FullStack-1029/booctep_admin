from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

# Create your models here.

class User(models.Model):
    password = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    last_login = models.DateTimeField(null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    receive_notifications = models.BooleanField(default=True)
    date_joined = models.DateTimeField(null=True, blank=True)
    first_name = models.CharField(max_length=200, null=True, blank=True)
    last_name = models.CharField( max_length=200, null=True, blank=True)
    phone_number = models.CharField(max_length=200, null=True, blank=True)
    image = models.TextField(null=True, blank=True)
    group_id = models.IntegerField(null=True, max_length=3)
