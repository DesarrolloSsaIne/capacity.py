from django import forms
from apps.periodicidad.models import Glo_Periodicidad

class periodicidadForm(forms.ModelForm):

    class Meta:
        model = Glo_Periodicidad

        fields = [
            'descripcion_periodicidad',


        ]


        widgets = {

            'descripcion_periodicidad': forms.TextInput(attrs={'class': 'form-control'}),

        }

