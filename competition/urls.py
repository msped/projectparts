from django.conf.urls import url
from .views import get_current_ticket_amount, winners

urlpatterns = [
    url(r'get_current/', get_current_ticket_amount, name="get_current_tickets"),
    url(r'winners/', winners, name="winners"),
]
