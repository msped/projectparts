import datetime
from django import forms

class PaymentForm(forms.Form):
    """Payment form for stripe"""
    now = datetime.datetime.now()
    MONTH_CHOICES = [(i, i) for i in range(1, 13)]
    YEAR_CHOICES = [(i, i) for i in range(now.year, now.year + 16)]

    credit_card_number = forms.CharField(label='Card number', required=False)
    cvv = forms.CharField(label='Security code (CVV)', max_length=3, required=False)
    expiry_month = forms.ChoiceField(label='Month', choices=MONTH_CHOICES, required=False)
    expiry_year = forms.ChoiceField(label='Year', choices=YEAR_CHOICES, required=False)
    stripe_id = forms.CharField(widget=forms.HiddenInput)
