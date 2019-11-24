from django.core.mail import send_mail
from django.template import loader
from django.utils.html import strip_tags

def email_order(request, orders, total):
    """Send out email to user with the order details"""
    html_email = loader.render_to_string(
        'email_templates/order_complete.html',
        {'order': orders, 'total': total, 'user': request.user.first_name}
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
