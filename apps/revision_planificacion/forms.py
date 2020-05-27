from django import forms
from apps.valida_plan2.models import  Ges_Controlador

class PlanUpdateForm(forms.ModelForm):

    class Meta:
        model = Ges_Controlador

        fields = [
            'estado_flujo',
        ]


        widgets = {

            'estado_flujo': forms.TextInput(attrs={'class': 'form-control'}),

        }