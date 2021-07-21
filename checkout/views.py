from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import stripe
from competition.models import Competition
from cart.models import Order
from .utils import (
    customer_paid,
    is_user_answer_correct
)

# Create your views here.

stripe.api_key = settings.STRIPE_SECRET

class Checkout(View):
    """Shows checkout page and handles checkout with stripe / DB changes"""
    template_name = 'checkout.html'
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(Checkout, self).dispatch(request, *args, **kwargs)

    def getComp(self):
        comp = Competition.objects.get(is_active=True)
        return comp

    def getOrder(self, user):
        try:
            order = Order.objects.get(user=user, ordered=False)
        except Order.DoesNotExist:
            order = None
        return order

    def get(self, request):
        order = self.getOrder(request.user.id)
        comp = self.getComp()
        if order is None:
            messages.error(
                request,
                "You have no tickets to checkout."
            )
            return redirect('products')
        else:
            context = {
            'user': request.user,
            'orders': order,
            'comp': comp
        }
        return render(request, self.template_name, context)
    
    def post(self, request):
        order = self.getOrder(request.user.id)
        comp = self.getComp()
        user_answer = request.POST.get('user-answer')
        if order is None:
            messages.error(request,
            'You have no active order.')
            return redirect('products')
        elif user_answer is None:
            messages.error(
                request,
                "Please select an answer to the question at the bottom of the page"
            )
            return redirect('checkout')
        else:
            total = order.get_total()
            tickets = order.ticket_amount()
            if tickets > comp.tickets_left:
                messages.error(
                    request,
                    """The amount of tickets you have ordered, {}, is greater
                        than what is left in the competition, {}.""".format(
                            tickets,
                            comp.tickets_left
                        )
                )
                return redirect('view_cart')
            else:
                intent = stripe.PaymentIntent.create(
                    amount=int(total * 100),
                    currency='gbp'
                )
                user_correct = is_user_answer_correct(user_answer, comp)
                payment_id = intent.id
                client_secret = intent.client_secret
                customer_paid(request, user_correct, tickets, total, payment_id)
                return HttpResponse(client_secret)

class checkoutComplete(View):
    """View to be displayed when the checkout has been completed"""
    template_name = 'checkout_complete.html'
    def get(self, request):
        order_id = request.session['order_id']
        order = Order.objects.get(id=order_id)
        del request.session['order_id']

        context = { 'order': order}
        return render(request, 'checkout_complete.html', context)