from django import forms

class ContactForm(forms.Form):
    """Form to be displayed on contact page"""
    email = forms.EmailField(required=True)
    subject = forms.CharField(required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)
