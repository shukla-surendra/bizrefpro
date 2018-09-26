from django import forms
from app.models import Executive

class ExecutiveForm(forms.ModelForm):
    class Meta:
        model = Executive
        fields = ['first_name', 'last_name', 'email', 'password','role']