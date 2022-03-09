from random import randint
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.template import loader
from django.utils.html import strip_tags
from checkout.models import Entries
from competition.utlis import (
    pick_competition_winner,
    check_for_new_competition,
)
from competition.models import Competition
from cart.models import Order

def get_entries(order):
    """Get all entries for an order and return as dict"""
    users_entries = {}
    for item in order.items.all():
        entries_per_order = []
        entries = Entries.objects.filter(orderItem=item.id)
        for ent in entries:
            entries_per_order.append(ent.ticket_number)
        n_order = {
            item.id: entries_per_order
        }
        users_entries.update(n_order)
    return users_entries

def email_order(request, order, user_correct):
    """Send out email to user with the order details"""
    users_entries = get_entries(order)

    html_email = loader.render_to_string(
        'email_templates/order_complete.html',
        {
            'order': order,
            'user': request.user.first_name,
            'user_correct': user_correct,
            'users_entries': users_entries
        }
    )
    message = strip_tags(html_email)
    send_mail(
        'Your Order for Project Parts',
        message=message,
        from_email='noreply@projectparts.com',
        fail_silently=False,
        connection=None,
        recipient_list=[str(request.user.email)],
        html_message=html_email
    )

def create_entries(order, user, comp, tickets, new_order):
    """Creates a users entries with a random number"""
    for item in order.items.all():
        tickets_per_order = item.quantity
        while tickets_per_order > 0:
            create = True
            while create:
                ticket_number = randint(1, comp.tickets)
                entry, created = Entries.objects.get_or_create(
                    defaults={
                        'user': user,
                        'orderItem': item
                    },
                    order=new_order,
                    competition_entry=comp,
                    ticket_number=ticket_number
                )
                if created:
                    tickets_per_order -= 1
                    create = False

    tickets_left = comp.tickets_left
    comp.tickets_left = tickets_left - tickets
    comp.save()

def is_user_answer_correct(user_answer, comp):
    """Checks if a user answer is correct"""
    user_correct = False
    if user_answer == comp.correct_answer:
        user_correct = True
    return user_correct

def update_orders(comp, order, user_correct, payment_id):
    """Update users orders in database"""
    users_orders = []
    for item in order.items.all():
        users_orders.append(item.id)
        item.is_paid = True
        item.save()
    order.related_competition = comp
    order.payment_id = payment_id
    order.order_date = timezone.now()
    order.answer_correct = user_correct
    order.ordered = True
    order.save()
    return order

def customer_paid(request, user_correct, tickets, total, payment_id):
    """Function handle all process if a customer has paid"""
    comp = Competition.objects.get(is_active=True)
    user = User.objects.get(id=request.user.id)
    order = Order.objects.get(user=user, ordered=False)
    new_order = update_orders(comp, order, user_correct, payment_id)
    if user_correct:
        create_entries(order, user, comp, tickets, new_order)
    email_order(request, order, user_correct)
    check_for_new_competition(comp)
    if comp.tickets_left == 0:
        pick_competition_winner()
    request.session['order_id'] = order.id
