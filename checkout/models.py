from django.db import models
from django.contrib.auth.models import User
from competition.models import Competition
from cart.models import OrderItem, Order

# Create your models here.

class Entries(models.Model):
    """Entries for a competition"""
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    competition_entry = models.ForeignKey(Competition, on_delete=models.DO_NOTHING)
    orderItem = models.ForeignKey(OrderItem, on_delete=models.DO_NOTHING, null=True)
    order = models.ForeignKey(Order, on_delete=models.DO_NOTHING, null=True)
    ticket_number = models.IntegerField()

    def __str__(self):
        return f'{self.competition_entry} | Ticket No: {self.ticket_number}'
