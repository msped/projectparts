from random import randint
from datetime import date
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.conf import settings
import stripe
from products.models import Product
from competition.utlis import new_competition, pick_competition_winner
from competition.models import Competition
from cart.models import Orders
from .utils import email_order, get_total
from .models import Entries
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
            tickets = 0

            for item in orders:
                tickets += item.quantity

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
                        for item in orders:
                            item.is_paid = True
                            item.order_date = date.today()
                            if user_answer == comp.correct_answer:
                                item.user_answer_correct = True
                            item.save()

                        user_correct = False
                        if user_answer == comp.correct_answer:
                            user_correct = True
                            for item in orders:
                                tickets_per_order = item.quantity
                                while tickets_per_order > 0:
                                    create = True
                                    while create:
                                        ticket_number = randint(1, comp.tickets)
                                        product = Product.objects.get(
                                            id=item.product.id
                                        )
                                        entry, created = Entries.objects.get_or_create(
                                            user=user,
                                            competition_entry=comp,
                                            order=item,
                                            product=product,
                                            ticket_number=ticket_number
                                        )
                                        if created:
                                            tickets_per_order -= 1
                                            create = False

                        tickets_left = comp.tickets_left
                        comp.tickets_left = tickets_left - tickets
                        comp.save()
                        email_order(request, orders, total, user_correct)
                        request.session['user_correct'] = user_correct
                        if comp.tickets_left < 500:
                            try:
                                new_comp = Competition.objects.get(
                                    next_competition=True
                                )
                            except new_comp.DoesNotExist:
                                new_competition()

                        if comp.tickets_left == 0:
                            pick_competition_winner()
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

def checkout_complete(request):
    """View to be displayed when the checkout has been completed"""

    user_correct = request.session['user_correct']
    print(user_correct)
    del request.session['user_correct']

    content = {
        'user_correct': user_correct
    }
    return render(request, 'checkout_complete.html', content)
