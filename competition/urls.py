from django.urls import path
from .views import get_current_ticket_amount, Winners

urlpatterns = [
    path('get_current/', get_current_ticket_amount, name="get_current_tickets"),
    path('winners/', Winners.as_view(), name="winners"),
]
