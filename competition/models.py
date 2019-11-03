from django.db import models

# Create your models here.

class Competition(models.Model):
    """Model for each competition"""
    tickets = models.IntegerField(default=4000)
    tickets_left = models.IntegerField(default=4000)
    question = models.CharField(max_length=200, default="Question")
    answer_1 = models.CharField(max_length=200, default="Answer 1")
    answer_2 = models.CharField(max_length=200, default="Answer 2")
    answer_3 = models.CharField(max_length=200, default="Answer 3")
    correct_answer = models.CharField(max_length=200, default="Correct Answer")
    is_active = models.BooleanField(default=False)
    next_competition = models.BooleanField(default=True)
    winner = models.ForeignKey(
        'checkout.Entries',
        on_delete=models.DO_NOTHING,
        null=True, blank=True
    )

    def __str__(self):
        if self.is_active:
            return f'Competition {self.id}: {self.tickets_left}'
        if self.tickets_left > 0:
            return f'Competition {self.id}: Pending'
        return f'Competition {self.id}: Ended'
