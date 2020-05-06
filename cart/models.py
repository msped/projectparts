from django.db import models
from django.contrib.auth.models import User
from django_simple_coupons.models import Coupon
from products.models import Product
from competition.models import Competition


# Create your models here.

class OrderItem(models.Model):
    """Model for a users order"""
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    quantity = models.IntegerField()
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.quantity} of {self.product.name}'

    def get_total_item_price(self):
        """Get total price for all tickets"""
        return self.quantity * self.product.ticket_price

    def get_final_price(self):
        """Get price of all including coupon code"""
        return self.get_total_item_price()

class Order(models.Model):
    """Model for an order"""
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    related_competition = models.ForeignKey(
        Competition,
        on_delete=models.SET_NULL,
        null=True
    )
    answer_correct = models.BooleanField(default=False)
    items = models.ManyToManyField(OrderItem)
    order_date = models.DateTimeField()
    payment_id = models.CharField(max_length=50)
    ordered = models.BooleanField(default=False)
    coupon = models.ForeignKey(
        Coupon,
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )

    def __str__(self):
        return f'{self.pk} | {self.order_date}'

    def get_total(self):
        total = 0
        for item in self.items.all():
            total += item.get_final_price()
        if self.coupon:
            total = total - ((total * self.coupon.discount.value) / 100)
        return total

    def show_savings(self):
        total = 0
        for item in self.items.all():
            total += item.get_final_price()
        saving_amount = (total * self.coupon.discount.value) / 100
        return saving_amount

    def ticket_amount(self):
        tickets = 0 
        for item in self.items.all():
            tickets += item.quantity
        return tickets
