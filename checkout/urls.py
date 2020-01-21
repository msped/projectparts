from django.conf.urls import url
from .views import checkout, checkout_complete

urlpatterns = [
    url(r'^$', checkout, name="checkout"),
    url(r'complete/', checkout_complete, name="checkout_complete")
]
