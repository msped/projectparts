from django.urls import path
from .views import (
    Cart,
    addCoupon,
    add_to_cart,
    decreaseItem,
    increaseItem,
    removeCoupon,
    remove_item,
)

urlpatterns = [
    path('', Cart.as_view(), name='view_cart'),
    path('add/', add_to_cart, name='add_to_cart'),
    path('add_one/<str:order_id>', increaseItem.as_view(), name='increase_item'),
    path('remove_one/<str:order_id>', decreaseItem.as_view(), name='decrease_item'),
    path('remove/', remove_item, name='remove_item'),
    path('add_coupon/', addCoupon.as_view(), name='add_coupon'),
    path('remove_coupon/', removeCoupon.as_view(), name='remove_coupon'),
]
