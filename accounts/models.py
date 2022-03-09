from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    """Information relating to a single user not in User model"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=11, blank=True, default='')
    address_line_1 = models.CharField(max_length=40, blank=True, default='')
    address_line_2 = models.CharField(max_length=40, blank=True, default='')
    town_city = models.CharField(max_length=40, blank=True, default='')
    county = models.CharField(max_length=40, blank=True, default='')
    country = models.CharField(max_length=40, blank=True, default='')
    postcode = models.CharField(max_length=10, blank=True, default='')
