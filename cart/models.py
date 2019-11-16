from django.db import models
from django.contrib.auth.models import User
from products.models import Product
from competition.models import Competition


# Create your models here.

class Orders(models.Model):
    """Model for users order / cart"""
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    related_competition = models.ForeignKey(Competition, on_delete=models.DO_NOTHING)
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=7, decimal_places=2, null=True)
    is_paid = models.BooleanField(default=False)
    user_answer_correct = models.BooleanField(default=False)
    order_date = models.DateField(null=True)

    def __str__(self):
        return f'Order {self.id} - Paid {self.is_paid}'
