from django.urls import path
from .views import CurrentTicketAmount, Winners

urlpatterns = [
    path('get_current/', CurrentTicketAmount.as_view(), name="get_current_tickets"),
    path('winners/', Winners.as_view(), name="winners"),
]
