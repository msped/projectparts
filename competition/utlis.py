from random import randint
from django.core.mail import mail_admins, send_mass_mail
from django.template import loader
from django.utils.html import strip_tags
from checkout.models import Entries
from .models import Competition

def new_competition():
    """Automatically create new competition when current competition
    is nearing completion"""
    Competition().save()

    # Send e-mail to admin to alert of new competition creation
    html_message = loader.render_to_string(
        'email_templates/admin_email.html'
        )
    message = strip_tags(html_message)
    mail_admins(
        'New Competition has been created.',
        message,
        fail_silently=True,
        connection=None,
        html_message=html_message
    )

def check_for_new_competition(comp):
    """"Check if the next competition has been created, if not create one"""
    if comp.tickets_left < 500:
        try:
            Competition.objects.get(
                next_competition=True
            )
        except Competition.DoesNotExist:
            new_competition()


def end_of_competition_emails(current_comp, winning_ticket):
    """Sends out e-mails at the end of a competition to players and winner"""
    comp_entries = Entries.objects.filter(competition_entry=current_comp.id)
    winners_email = [winning_ticket.user.email,]
    recipient_list = []
    for entry in comp_entries:
        if winners_email != entry.user.email:
            recipient_list.append(entry.user.email)

    message = """
    Hurah!\n
    A winner has been chosen for competition {}, congratulations to {} {}! \n
    They have won a {}.\n
    Good luck next time!\n
    Many Thanks, \n
    Project Parts Team
    """.format(
        current_comp.id,
        winning_ticket.user.first_name,
        winning_ticket.user.last_name,
        winning_ticket.order.product
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
    Please sit tight, we will contact you within 2 working days.\n
    Again, congratulations and thanks for playing!\n
    Many Thanks,\n
    Project Parts Team
    """.format(
        current_comp.id,
        winning_ticket.ticket_number,
        winning_ticket.order.product
    )

    winner = (
        'Congratulations, you won!',
        winner_message,
        'noreply@projectparts.com',
        winners_email
    )
    send_mass_mail((participants, winner), fail_silently=True)

def pick_competition_winner():
    """Get Competition winner and send out emails"""
    current_comp = Competition.objects.get(is_active=True, tickets_left=0)

    # Change to next competition to minimize
    current_comp.is_active = False
    current_comp.save()
    next_comp = Competition.objects.get(next_competition=True)
    next_comp.is_active = True
    next_comp.next_competition = False
    next_comp.save()

    r_number = randint(1, current_comp.tickets)
    winning_ticket = Entries.objects.get(
        competition_entry=current_comp.id,
        ticket_number=r_number
    )
    current_comp.winner = winning_ticket
    current_comp.save()

    end_of_competition_emails(current_comp, winning_ticket)
