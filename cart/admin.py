from django.contrib import admin
from .models import Order, OrderItem

# Register your models here.

class OrderFilter(admin.ModelAdmin):
    """Makes orders readonly in admin"""
    readonly_fields = (
        'user',
        'related_competition',
        'answer_correct', 
        'items',
        'order_date',
        'payment_id',
        'coupon'
    )

    filter_horizontal = ('items', )

class OrderItemFilter(admin.ModelAdmin):
    """Makes orderitems readonly in admin"""
    readonly_fields = (
        'user',
        'product',
        'quantity', 
        'is_paid'
    )

admin.site.register(Order, OrderFilter)
admin.site.register(OrderItem, OrderItemFilter)
