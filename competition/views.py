from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from django.core.paginator import Paginator
from competition.models import Competition

# Create your views here.

class CurrentTicketAmount(View):
    def get(self, request):
        try:
            comp = Competition.objects.get(is_active=True)
            tickets_left = comp.tickets_left
        except Competition.DoesNotExist:
            tickets_left = "No Competition Active"
        return HttpResponse(tickets_left)

class Winners(View):
    template_name = 'winners.html'
    def get(self, request):
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

        return render(request, self.template_name, context)
