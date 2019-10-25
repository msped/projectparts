from django.db import models
from django.contrib.auth.models import User
from products.models import Product
from competition.models import Competition

# Create your models here.

class Enteries(models.Model):
    """Model for competition enteries / cart item for registered users"""
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    competition = models.ForeignKey(Competition, on_delete=models.DO_NOTHING)
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    ticket_number = models.ForeignKey(Product, on_delete=models.DO_NOTHING, null=True)
    is_paid = models.BooleanField(default=False)
