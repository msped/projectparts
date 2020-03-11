from random import randint
from datetime import date
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.template import loader
from django.utils.html import strip_tags
from checkout.models import Entries
from competition.utlis import (
    pick_competition_winner,
    check_for_new_competition,
)

def email_order(request, orders, total, user_correct):
    """Send out email to user with the order details"""
    users_entries = {}
    for item in orders:
        entries_per_order = []
        entries = Entries.objects.filter(order=item.id)
        for ent in entries:
            entries_per_order.append(ent.ticket_number)
        n_order = {
            item.id: entries_per_order
        }
        users_entries.update(n_order)

    html_email = loader.render_to_string(
        'email_templates/order_complete.html',
        {
            'order': orders,
            'total': total,
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
        fail_silently=True,
        connection=None,
        recipient_list=[str(request.user.email)],
        html_message=html_email
    )

def get_total(orders):
    """Gets total for orders"""
    total = 0
    for item in orders:
        total += item.quantity * item.product.ticket_price

    return total

def create_entries(orders, user, comp, tickets):
    """Creates a users entries with a random number"""
    for item in orders:
        tickets_per_order = item.quantity
        while tickets_per_order > 0:
            create = True
            while create:
                ticket_number = randint(1, comp.tickets)
                entry, created = Entries.objects.get_or_create(
                    defaults={
                        'user': user,
                        'order': item
                    },
                    competition_entry=comp,
                    ticket_number=ticket_number
                )
                if created:
                    tickets_per_order -= 1
                    create = False

    tickets_left = comp.tickets_left
    comp.tickets_left = tickets_left - tickets
    comp.save()

def is_user_answer_correct(request, user_answer, comp):
    """Checks if a user answer is correct"""
    user_correct = False
    if user_answer == comp.correct_answer:
        user_correct = True
    request.session['user_correct'] = user_correct
    return user_correct

def get_users_tickets(orders):
    """Add up all of a users tickets"""
    tickets = 0
    for order in orders:
        tickets += order.quantity
    return tickets

def update_orders(orders, user_correct):
    """Update users orders in database"""
    for item in orders:
        item.is_paid = True
        item.order_date = date.today()
        if user_correct:
            item.user_answer_correct = True
        item.save()

def customer_paid(request, orders, user_correct, comp, tickets, total):
    """Function handle all process if a customer has paid"""
    user = User.objects.get(id=request.user.id)
    update_orders(orders, user_correct)
    if user_correct:
        create_entries(orders, user, comp, tickets)
    email_order(request, orders, total, user_correct)
    check_for_new_competition(comp)
    if comp.tickets_left == 0:
        pick_competition_winner()
