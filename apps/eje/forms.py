from django import forms
from apps.eje.models import Ges_Ejes

class EjeForm(forms.ModelForm):


     class Meta:
        model = Ges_Ejes

        fields = [
            'descripcion_eje',
            'id_eje',
        ]
        labels = {
            'descripcion_eje': 'Nombre',
            'id_eje': 'ID',
        }

        widgets = {
            'id_eje': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion_eje': forms.TextInput(attrs={'class': 'form-control'}),


        }
