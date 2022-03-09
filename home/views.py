from django.shortcuts import render
from django.views import View
from competition.models import Competition

# Create your views here.

class Home(View):
    
    def get(self, request):
        try:
            comp = Competition.objects.get(is_active=True)
            tickets_left = comp.tickets_left
        except Competition.DoesNotExist:
            tickets_left = "No Competition Active"

        content = {
            'tickets_left': tickets_left
        }
        return render(request, 'home.html', content)
