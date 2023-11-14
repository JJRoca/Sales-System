from django import forms
from .models import Client

class ClientForm(forms.ModelForm):
    """ClientForm definition."""
    class Meta:
        model = Client
        fields = ["name","surnames","dni","date_birthday","address","gender"]

        widgets = {
            'name': forms.TextInput(attrs={"class": "form-control", "id": "name", "name": "name", "placeholder": "Enter your namess"}),
            'surnames': forms.TextInput(attrs={"class": "form-control", "id": "surnames", "name": "surnames", "placeholder": "Enter your Last Name"}),
            'dni': forms.TextInput(attrs={"class": "form-control", "id": "dni", "name": "dni", "placeholder": "Enter your DNI"}),
            'date_birthday': forms.DateInput(attrs={"class": "form-control", "id": "date_birthday", "name": "date_birthday"}),
            'address': forms.TextInput(attrs={"class": "form-control", "id": "address", "name": "address", 'placeholder': 'Enter your address'}),
            'gender': forms.Select(attrs={"class": "form-control", "id": "gender", "name": "gender"}),
        }
