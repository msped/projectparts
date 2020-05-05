from django.conf.urls import url
from .views import (
    view_cart,
    add_to_cart,
    remove_item,
    decrease_item,
    increase_item,
    add_coupon,
    remove_coupon
)

urlpatterns = [
    url(r'^$', view_cart, name='view_cart'),
    url(r'^add/', add_to_cart, name='add_to_cart'),
    url(r'^add_one/(?P<order_id>\d+)', increase_item, name='increase_item'),
    url(r'^remove_one/(?P<order_id>\d+)', decrease_item, name='decrease_item'),
    url(r'^remove/', remove_item, name='remove_item'),
    url(r'^add_coupon/', add_coupon, name='add_coupon'),
    url(r'^remove_coupon/', remove_coupon, name='remove_coupon'),
]
