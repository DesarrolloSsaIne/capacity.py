from django import forms
from apps.familia_cargo.models import Glo_FamiliaCargo
from django.contrib.auth.models import User

class familiaCargoForm(forms.ModelForm):

    class Meta:
        model = Glo_FamiliaCargo

        fields = [

            'descripcion_familiacargo',
        ]


        widgets = {

            'descripcion_familiacargo': forms.TextInput(attrs={'class': 'form-control'}),
        }