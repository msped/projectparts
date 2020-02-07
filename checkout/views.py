from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.conf import settings
import stripe
from competition.models import Competition
from cart.models import Orders
from cart.contexts  import cart_contents
from accounts.contexts import check_profile
from .utils import (
    get_total,
    get_users_tickets,
    customer_paid
)
from .forms import PaymentForm

# Create your views here.

stripe.api_key = settings.STRIPE_SECRET

@login_required
def checkout(request):
    """Shows checkout page and handles checkout with stripe / DB changes"""
    comp = Competition.objects.get(is_active=True)
    user = User.objects.get(id=request.user.id)
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

    profile_check = check_profile(request)
    if profile_check['profile_incomplete']:
        messages.error(
            request,
            "Please fil out your details before placing an order. " +
            "(So we can contact you if you win!)"
        )
        return redirect('profile')

    if request.method == "POST":
        payment_form = PaymentForm(request.POST)
        user_answer = request.POST.get('user-answer')

        if user_answer is None:
            messages.error(
                request,
                "Please select an answer to the question at the bottom of the page"
            )
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
            else:
                if payment_form.is_valid():
                    try:
                        customer = stripe.Charge.create(
                            amount=int(total * 100),
                            currency="gbp",
                            source='tok_visa'
                        )
                    except stripe.error.CardError:
                        messages.error(request, "Your card has been declined.")

                    if customer.paid:
                        customer_paid(
                            request,
                            orders,
                            user_answer,
                            comp,
                            tickets,
                            user,
                            total
                        )
                        return redirect('checkout_complete')
                else:
                    messages.error(
                        request,
                        "We are unable to take payment from that card."
                    )
    else:
        payment_form = PaymentForm()

    content = {
        'user': request.user,
        'orders': orders,
        'comp': comp,
        'payment_form': payment_form
    }
    return render(request, 'checkout.html', content)

@login_required
def checkout_complete(request):
    """View to be displayed when the checkout has been completed"""

    user_correct = request.session['user_correct']
    del request.session['user_correct']

    content = {
        'user_correct': user_correct
    }
    return render(request, 'checkout_complete.html', content)
