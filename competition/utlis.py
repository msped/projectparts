from django.core.mail import mail_admins
from django.template import loader
from .models import Competition

def new_competition():
    """Automatically create new competition when current competition
    is nearing completion"""
    Competition().save()

    # Send e-mail to admin to alert of new competition creation
    message = """Hello,\n\n A new competition has been created ready for when
    the current competition ends.\n\n Please go to the admin panel to add the
    question and associated answers.\n\n Regards,\n Project Parts"""
    mail_admins(
        'New Competition has been created.',
        message,
        fail_silently=True,
        connection=None,
        html_message=loader.render_to_string(
            'admin_email.html'
        )
    )

def get_current_ticket_amount():
    """Get tickets left in current competition for homepage"""
    comp = Competition.objects.get(is_active=True)
    return comp.tickets_left
