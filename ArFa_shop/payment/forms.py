# forms.py
from django import forms

class CardPaymentForm(forms.Form):
    card_number = forms.CharField(max_length=16, min_length=16, label='Card Number')
    amount = forms.IntegerField(label='Amount')