from django.shortcuts import render
from competition.models import Competition

# Create your views here.

def home(request):
    comp = Competition.objects.get(is_active=True)

    content = {
        'tickets_left': comp.tickets_left
    }
    return render(request, 'home.html', content)
