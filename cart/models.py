from django.db import models
from django.contrib.auth.models import User
from products.models import Product
from competition.models import Competition


# Create your models here.

class Enteries(models.Model):
    """Model for competition enteries / cart item for registered users"""
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING)
    related_competition = models.OneToOneField(Competition, on_delete=models.DO_NOTHING)
    product = models.OneToOneField(Product, on_delete=models.DO_NOTHING)
    ticket_number = models.IntegerField(null=True)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f'Number: {self.ticket_number} by User: {self.user}'
