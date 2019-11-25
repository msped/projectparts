from random import randint
from datetime import datetime
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.conf import settings
import stripe
from competition.utlis import new_competition
from competition.models import Competition
from cart.models import Orders
from .utils import email_order
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
            tickets = 0

            if payment_form.is_valid():
                for item in orders:
                    total += item.quantity * item.product.ticket_price
                    tickets += item.quantity
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
                    user_correct = False
                    if user_answer == comp.correct_answer:
                        user_correct = True
                        for item in orders:
                            tickets_per_order = item.quantity
                            while tickets_per_order > 0:
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
                                        tickets_per_order -= 1
                                        create = False

                    tickets_left = comp.tickets_left
                    comp.tickets_left = tickets_left - tickets
                    comp.save()
                    email_order(request, orders, total, user_correct)
                    if comp.tickets_left < 500:
                        try:
                            new_comp = Competition.objects.get(
                                next_competition=True
                            )
                        except new_comp.DoesNotExist:
                            new_competition()
                    return redirect('checkout_complete', orders)
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

@login_required
def checkout_complete(request, orders):
    """View to be displayed when the checkout has been completed"""
    comp = Competition.objects.get(is_active=True)
    users_entries = {}
    user_correct_answer = False
    for item in orders:
        if item.user_answer_correct:
            user_correct_answer = True
        entries_per_order = []
        entries = Entries.objects.filter(order=item.id)
        for ent in entries:
            entries_per_order.append(ent.ticket_number)
        n_order = {
            item.id: entries_per_order
        }
        users_entries.update(n_order)

    content = {
        'user': request.user,
        'order': orders,
        'user_entries': users_entries,
        'user_correct_answer': user_correct_answer,
        'correct_answer': comp.correct_answer
    }
    return render(request, 'checkout_complete.html', content)