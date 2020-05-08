from django import forms
from apps.controlador.models import Ges_Controlador
from apps.jefaturas.models import Ges_Jefatura as Gj

class controladorFlujoForm(forms.ModelForm):



    class Meta:
        model = Ges_Controlador

        fields = [
            'id_jefatura',

        ]


        widgets = {

            'id_jefatura': forms.Select(attrs={'class': 'form-control', 'id':'siteID'}),


        }

class controladorFlujoForm(forms.ModelForm):



    class Meta:
        model = Ges_Controlador

        fields = [
            'id_jefatura',

        ]


        widgets = {

            'id_jefatura': forms.Select(attrs={'class': 'form-control', 'id':'siteID'}),


        }
class GestionControladorUpdateForm(forms.ModelForm):

    def __init__(self,nivel_jefatura ,*args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(GestionControladorUpdateForm, self).__init__(*args, **kwargs)
        self.fields['jefatura_primerarevision'].queryset = Gj.objects.filter(id_nivel_id=nivel_jefatura)



    class Meta:
        model = Ges_Controlador
        fields = [
            'estado_flujo',
            'id_jefatura',
            'jefatura_primerarevision'

        ]

        widgets = {
            'estado_flujo': forms.Select(attrs={'class': 'form-control', 'readonly':'readonly'}),
            'jefatura_primerarevision': forms.Select(attrs={'class': 'form-control'}),
            'id_jefatura': forms.Select(attrs={'class': 'form-control', 'readonly':'readonly'}),
        }
