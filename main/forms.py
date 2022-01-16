from .models import City
from django.forms import ModelForm, TextInput


class CityForm(ModelForm):
    class Meta:
        model = City
        fields = ["city"]
        widgets = {"city": TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Wpisz miasto'})
        }


