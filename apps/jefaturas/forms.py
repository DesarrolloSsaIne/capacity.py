from django import forms
from apps.jefaturas.models import Ges_Jefatura


class JefaturasForm(forms.ModelForm):

    class Meta:
        model = Ges_Jefatura


        fields = [

            'id_user',
            'id_nivel',




        ]

        widgets = {

            'id_user': forms.Select(attrs={'class': 'form-control', 'id': 'siteID', 'style':'width:550px;'}),

            'id_nivel': forms.Select(attrs={'class': 'form-control', 'id': 'siteID2', 'style':'width:550px;'}),
        }
