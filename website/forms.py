from django.contrib.auth.models import User
from django import forms
from website.models import *

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'first_name', 'last_name',)

class ProductForm(forms.ModelForm):
    # producttypenames = ProductType.objects.raw("SELECT pt.name FROM website_producttype as pt")
    # product_type = forms.ChoiceField(choices=[(x, x) for x in producttypenames])

    class Meta:
        model = Product
        fields = ('title', 'description', 'price', 'quantity', 'productType')