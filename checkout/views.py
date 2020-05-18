from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.conf import settings
import stripe
from competition.models import Competition
from cart.models import Order
from .models import Entries
from .utils import (
    customer_paid,
    is_user_answer_correct
)

# Create your views here.

stripe.api_key = settings.STRIPE_SECRET

@login_required
def checkout(request):
    """Shows checkout page and handles checkout with stripe / DB changes"""
    comp = Competition.objects.get(is_active=True)
    order = Order.objects.get(user=request.user.id, ordered=False)

    if order.ticket_amount() == 0:
        messages.error(
            request,
            "You have no tickets to checkout."
        )
        return redirect('products')
    if request.method == "POST":
        user_answer = request.POST.get('user-answer')
        if user_answer is None:
            messages.error(
                request,
                "Please select an answer to the question at the bottom of the page"
            )
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
                user_correct = is_user_answer_correct(request, user_answer, comp)
                payment_id = intent.id
                client_secret = intent.client_secret
                customer_paid(request, user_correct, tickets, total, payment_id)
                return HttpResponse(client_secret)

    content = {
        'user': request.user,
        'orders': order,
        'comp': comp
    }
    return render(request, 'checkout.html', content)

@login_required
def checkout_complete(request):
    """View to be displayed when the checkout has been completed"""

    order_id = request.session['order_id']
    order = Order.objects.get(id=order_id)
    del request.session['order_id']

    content = {
        'order': order
    }
    return render(request, 'checkout_complete.html', content)
