from django import forms
from app.models import Business, User


class BusinessForm(forms.ModelForm):
    class Meta:
        model = Business
        fields = ['business_name', 'address1', 'address2','landmark','location','city','pincode','contact_prefix','first_name', 'last_name', 'designation','landline','contact_number','email','aboutus','title','categories','keyword','gst_no']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'email','phone','address1','city']


class UpdateProfileForm(forms.Form):
        name = forms.CharField(max_length=100)
        email = forms.EmailField(max_length=100)
        phone = forms.CharField(max_length=100)
        address1 = forms.CharField(max_length=100)
        address2 = forms.CharField(max_length=100, required=False)
        country = forms.CharField(max_length=100)
        reference_id = forms.CharField(max_length=50, required=False)
        state = forms.CharField(max_length=100)
        city = forms.CharField(max_length=100)
