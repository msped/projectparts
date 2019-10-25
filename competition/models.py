from django.db import models
from cart.models import Enteries

# Create your models here.


class Competition(models.Model):
    """Model for each competition"""
    tickets = models.IntegerField()
    tickets_left = models.IntegerField()
    question = models.CharField()
    answer_1 = models.CharField()
    answer_2 = models.CharField()
    answer_3 = models.CharField()
    correct_answer = models.CharField()
    is_active = models.BooleanField()
    winner = models.ForeignKey(Enteries, on_delete=models.DO_NOTHING, null=True)

    def __str__(self):
        if self.is_active:
            return f'Competition {self.id}: {self.tickets_left}'
        return f'Competition {self.id}: Ended'
