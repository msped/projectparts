from django.conf.urls import url
from .views import view_cart, add_to_cart, update_cart

urlpatterns = [
    url(r'^$', view_cart, name='view_cart'),
    url(r'^add/(?P<product_id>\d+)', add_to_cart, name='add_to_cart'),
    url(r'^adjust/(?P<product_id>\d+)', update_cart, name='update_cart'),
]
