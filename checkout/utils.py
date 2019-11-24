from django.core.mail import send_mail
from django.template import loader
from django.utils.html import strip_tags

def email_order(user_email, orders, total):
    """Send out email to user with the order details"""
    html_email = loader.render_to_string(
        'email_templates/order_complete.html',
        {'order': orders, 'total': total}
    )
    message = strip_tags(html_email)
    send_mail(
        'Your Order for Project Parts',
        message=message,
        from_email='noreply@projectparts.com',
        fail_silently=True,
        connection=None,
        recipient_list=[str(user_email)],
        html_message=html_email
    )
