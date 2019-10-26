from django.db import models

# Create your models here.

class Competition(models.Model):
    """Model for each competition"""
    tickets = models.IntegerField(default=4000)
    tickets_left = models.IntegerField(default=4000)
    question = models.CharField(max_length=200)
    answer_1 = models.CharField(max_length=200)
    answer_2 = models.CharField(max_length=200)
    answer_3 = models.CharField(max_length=200)
    correct_answer = models.CharField(max_length=200)
    is_active = models.BooleanField(default=False)
    winner = models.ForeignKey('cart.Enteries', on_delete=models.DO_NOTHING, null=True)

    def __str__(self):
        if self.is_active:
            return f'Competition {self.id}: {self.tickets_left}'
        return f'Competition {self.id}: Ended'
