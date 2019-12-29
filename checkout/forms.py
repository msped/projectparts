from django import forms

class PaymentForm(forms.Form):
    """Payment form for stripe"""
    MONTH_CHOICES = [(i, i) for i in range(1, 13)]
    YEAR_CHOICES = [(i, i) for i in range(2016, 2075)]

    credit_card_number = forms.CharField(label='Card number', required=True)
    cvv = forms.CharField(label='Security code (CVV)', required=True)
    expiry_month = forms.ChoiceField(label='Month', choices=MONTH_CHOICES, required=True)
    expiry_year = forms.ChoiceField(label='Year', choices=YEAR_CHOICES, required=True)
    stripe_id = forms.CharField(widget=forms.HiddenInput)
