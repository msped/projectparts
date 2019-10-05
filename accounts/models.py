from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    """Information relating to a single user not in User model"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=11, blank=False)
    
class BillingShipping(models.Model):
    """Billing and Shipping for a user"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address_line_1 = models.CharField(max_length=40, blank=False)
    address_line_2 = models.CharField(max_length=40, blank=True)
    town_city = models.CharField(max_length=40, blank=False)
    county = models.CharField(max_length=40, blank=False)
    country = models.CharField(max_length=40, blank=False)
    postcode = models.CharField(max_length=10, blank=False)

