from django.shortcuts import render
from django.http import JsonResponse
from django.core.mail import send_mail
from projectparts.settings import EMAIL_HOST_USER
from .forms import ContactForm

# Create your views here.

def contact_view(request):
    """View contact page"""
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']

            send_mail(subject, message, email, [EMAIL_HOST_USER])

            data = {
                'sent': True
            }
        else:
            data = {
                'sent': False,
                'error': "Invalid Form"
            }
        return JsonResponse(data)
    else:
        form = ContactForm()

        content = {
            'form': form,
        }
    return render(request, "contactus.html", content)
    