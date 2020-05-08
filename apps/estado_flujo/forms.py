from django import forms
from apps.estado_flujo.models import Glo_EstadoFlujo

class estadoFlujoForm(forms.ModelForm):

    class Meta:
        model = Glo_EstadoFlujo

        fields = [
            'descripcion_estado',
            'estado',

        ]


        widgets = {

            'descripcion_estado': forms.TextInput(attrs={'class': 'form-control'}),
            'estado': forms.TextInput(attrs={'class': 'form-control','type':'number'}),

        }

