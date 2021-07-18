from django.contrib.auth.decorators import login_required
from django.urls import path
from .views import Checkout, checkoutComplete

urlpatterns = [
    path('', login_required(Checkout.as_view()), name="checkout"),
    path('complete/', login_required(checkoutComplete.as_view()), name="checkout_complete")
]
