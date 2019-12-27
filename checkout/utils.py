from django.core.mail import send_mail
from django.template import loader
from django.utils.html import strip_tags
from checkout.models import Entries

def email_order(request, orders, total, user_correct):
    """Send out email to user with the order details"""
    user_correct = False
    users_entries = {}
    for item in orders:
        if item.user_answer_correct:
            user_correct = True
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
