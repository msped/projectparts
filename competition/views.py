from django.http import HttpResponse
from django.shortcuts import render
from django.core.paginator import Paginator
from competition.models import Competition

# Create your views here.

def get_current_ticket_amount(request):
    """Get tickets left in current competition for homepage"""
    try:
        comp = Competition.objects.get(is_active=True)
        tickets_left = comp.tickets_left
    except Competition.DoesNotExist:
        tickets_left = "No Competition Acitve"
    return HttpResponse(tickets_left)

def winners(request):
    """Page to display previous winners for the competition"""

    previous_comp = Competition.objects.filter(
        is_active=False,
        winner__isnull=False
    ).order_by('-id')

    paginator = Paginator(previous_comp, 15)
    page = request.GET.get('page')
    prev_comp = paginator.get_page(page)

    context = {
        'prev_comp': prev_comp
    }

    return render(request, 'winners.html', context)
