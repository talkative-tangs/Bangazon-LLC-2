from django.contrib.auth.models import User
from django import forms
from website.models import *

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'first_name', 'last_name',)

class ProductForm(forms.ModelForm):
    quantity = forms.DecimalField(min_value=1)
    price = forms.DecimalField(min_value=0.01, max_value=10000)

    class Meta:
        model = Product
        fields = ('title', 'description', 'price', 'quantity', 'productType')
        labels = {'productType': 'Product Type'}

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
