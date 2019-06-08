from django import forms
from .models import User, Contact


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'email', 'phone', 'password']


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'contact', 'message']


class RefererForm(forms.Form):
    otp = forms.CharField(max_length=30)
    referer_email = forms.EmailField(max_length=150)
    name = forms.CharField(max_length=30)
    email = forms.EmailField(max_length=150, required=False)
    contact = forms.CharField(max_length=10)



