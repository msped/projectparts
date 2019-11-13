from random import randint
from django.shortcuts import render, reverse, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.conf import settings
from datetime import datetime
import stripe
from competition.models import Competition
from cart.models import Orders
from .models import Entries
from .forms import PaymentForm

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

    if request.method == "POST":
        payment_form = PaymentForm(request.POST)
        user_answer = request.POST.get('user-answer')

        if user_answer is None:
            messages.error(
                request,
                "Please select an answer to the question at the bottom of the page"
            )
        else:

            total = 0

            if payment_form.is_valid():
                for item in orders:
                    total += item.quantity * item.product.ticket_price
                    item.is_paid = True
                    item.order_date = datetime.today().strftime('%Y-%M-%D')
                    if user_answer == comp.correct_answer:
                        item.user_answer_correct = True
                    item.save()
                try:
                    customer = stripe.Charge.create(
                        amount=int(total * 100),
                        curreny="GBP",
                        description=request.user.email,
                        card=payment_form.cleaned_data['stripe_id']
                    )
                except stripe.error.CardError:
                    messages.error(request, "Your card has been declined.")

                if customer.paid:
                    if user_answer == comp.correct_answer:
                        for item in orders:
                            create = True
                            while create:
                                ticket_number = randint(1, comp.tickets)
                                entry, created = Entries.objects.get_or_create(
                                    user=request.user.id,
                                    competition_entry=comp.id,
                                    product=item.product.id,
                                    ticket_number=ticket_number
                                )
                                if created:
                                    create = False
            else:
                messages.error(
                    request,
                    "We are unable to take payment from that card"
                )
    else:
        payment_form = PaymentForm()

    content = {
        'user': request.user,
        'orders': orders,
        'comp': comp,
        'payment_form': payment_form,
        'pushlishable': settings.STRIPE_PUBLISHABLE
    }
    return render(request, 'checkout.html', content)
