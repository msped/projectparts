from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.conf import settings
import stripe
from competition.models import Competition
from cart.models import Orders
from cart.contexts  import cart_contents
from .utils import (
    get_total,
    get_users_tickets,
    customer_paid,
    is_user_answer_correct
)

# Create your views here.

stripe.api_key = settings.STRIPE_SECRET

@login_required
def checkout(request):
    """Shows checkout page and handles checkout with stripe / DB changes"""
    comp = Competition.objects.get(is_active=True)
    orders = Orders.objects.filter(
        user=request.user.id,
        is_paid=False,
        related_competition=comp.id
    )

    cart_count = cart_contents(request)

    if cart_count['product_count'] == 0:
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
            return redirect('checkout')
        else:
            total = get_total(orders)
            tickets = get_users_tickets(orders)

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
                    currency='gbp',
                    # Verify your integration in this guide by including this parameter
                    metadata={'integration_check': 'accept_a_payment'},
                )
                is_user_answer_correct(request, user_answer, comp)
                client_secret = intent.client_secret
                return HttpResponse(client_secret)

    content = {
        'user': request.user,
        'orders': orders,
        'comp': comp
    }
    return render(request, 'checkout.html', content)

@login_required
def checkout_complete(request):
    """View to be displayed when the checkout has been completed"""
    comp = Competition.objects.get(is_active=True)
    orders = Orders.objects.filter(
        user=request.user.id,
        is_paid=False,
        related_competition=comp.id
    )

    tickets = get_users_tickets(orders)
    total = get_total(orders)

    user_correct = request.session['user_correct']
    if user_correct:
        customer_paid(
            request,
            orders,
            user_correct,
            comp,
            tickets,
            total
        )

    del request.session['user_correct']
    content = {
        'user_correct': user_correct
    }
    return render(request, 'checkout_complete.html', content)
