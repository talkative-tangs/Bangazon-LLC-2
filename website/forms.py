from django.contrib.auth.models import User
from django import forms
from website.models import *

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'first_name', 'last_name',)

class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ('title', 'description', 'price', 'quantity','productType')

class PaymentForm(forms.ModelForm):
    '''form for adding a payment type'''

    class Meta:
        model = PaymentType
        fields = (
            'name',
            'accountNum',
        )
        labels = {
            'name': 'Payment Type Name',
            'accountNum': 'Account Number',
            }
       
