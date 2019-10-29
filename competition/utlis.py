from random import randint
from django.core.mail import mail_admins, send_mass_mail
from django.template import loader
from cart.models import Enteries
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
            'email_templates/admin_email.html'
        )
    )

def get_current_ticket_amount():
    """Get tickets left in current competition for homepage"""
    comp = Competition.objects.get(is_active=True)
    return comp.tickets_left

def pick_competition_winner():
    """Get Competition winner and send out emails"""
    current_comp = Competition.objects.get(is_active=True, tickets_left=0)
    r_number = randint(1, current_comp.tickets)
    winning_ticket = Enteries.objects.get(
        related_competition=current_comp.id,
        ticket_number=r_number,
        is_paid=True
    )
    current_comp.winner = winning_ticket.id
    current_comp.save()

    winners_email = winning_ticket.user.email

    enteries = Enteries.objects.get(related_competition=current_comp.id)
    recipient_list = []
    for entry in enteries:
        user_email = entry.user.email
        if winners_email != user_email:
            recipient_list.append(user_email)

    message = """"
    Hurah!\n
    A winner has been chosen for competition {}, congratulations to {} {}! \n
    They have won a {} for their {}.\n
    Good luck next time!\n
    Many Thanks, \n
    Project Parts Team
    """.format(
        current_comp.id,
        winning_ticket.user.first_name,
        winning_ticket.user.last_name,
        winning_ticket.product.name,
        winning_ticket.product.fits
    )
    participants = (
        'A winner has been chosen! A new competition has also started.',
        message,
        'noreply@projectparts.com',
        recipient_list
    )

    winner_message = """
    Congratulations, you won competition {}!\n
    Your winning number {} has won you {}.\n
    Please sit tight, we will contact you with 2 working days.\n
    Again, congratulations and thanks for playing!\n
    Many Thanks,\n
    Project Parts Team
    """.format(
        current_comp.id,
        winning_ticket.ticket_number,
        winning_ticket.product.name
    )

    winner = (
        'Congratulations, you won!',
        winner_message,
        'noreply@projectparts.com',
        winners_email
    )
    send_mass_mail((participants, winner), fail_silently=True)

    # Change to next competition
    current_comp.is_active = False
    current_comp.save()
    next_comp = Competition.objects.get(next_competition=True)
    next_comp.is_active = True
    next_comp.next_competition = False
    next_comp.save()
