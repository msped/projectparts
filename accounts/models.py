from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    """Information relating to a single user not in User model"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=11, blank=False, default='Phone Number')
    address_line_1 = models.CharField(max_length=40, blank=False, default='Address Line 1')
    address_line_2 = models.CharField(max_length=40, blank=True, default='Address Line 2')
    town_city = models.CharField(max_length=40, blank=False, default='Town / City')
    county = models.CharField(max_length=40, blank=False, default='County')
    country = models.CharField(max_length=40, blank=False, default='Country')
    postcode = models.CharField(max_length=10, blank=False, default='Postcode')
