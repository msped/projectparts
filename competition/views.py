from django.http import HttpResponse
from competition.models import Competition

# Create your views here.

def get_current_ticket_amount(request):
    """Get tickets left in current competition for homepage"""
    comp = Competition.objects.get(is_active=True)
    tickets_left = comp.tickets_left
    return HttpResponse(tickets_left)
