from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=11, blank=False)
    address_line_1 = models.CharField(max_length=40, blank=False)
    address_line_2 = models.CharField(max_length=40, blank=True)
    town_city = models.CharField(max_length=40, blank=False)
    county = models.CharField(max_length=40, blank=False)
    country = models.CharField(max_length=40, blank=False)
    postcode = models.CharField(max_length=10, blank=True)

    def __str__(self):
        return self.user.email