from django.db import models
from django.contrib.auth.models import User
from products.models import Product
from competition.models import Competition

# Create your models here.

class Entries(models.Model):
    """Entries for a competition"""
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    competition_entry = models.ForeignKey(Competition, on_delete=models.DO_NOTHING)
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    ticket_number = models.IntegerField()

    def __str__(self):
        return f'Comp: {self.competition_entry} | Ticket No: {self.ticket_number}'
