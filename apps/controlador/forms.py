from django import forms
from apps.controlador.models import Ges_Controlador
from apps.jefaturas.models import Ges_Jefatura
from apps.jefaturas.models import Ges_Jefatura as Gj
from django.contrib.auth.models import User, Group
from django.db.models import Q

class controladorFlujoForm(forms.ModelForm):

    def __init__(self, id_periodo ,*args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(controladorFlujoForm, self).__init__(*args, **kwargs)
        qs= Ges_Controlador.objects.all().values_list('id_jefatura', flat=True)


        jefaturas_pefiles = list(User.objects.values_list('id', flat=True).filter(groups__in=Group.objects.filter(Q(id='4') | Q(id='3'))))


        self.fields['id_jefatura'].queryset = Ges_Jefatura.objects.filter(id_periodo=id_periodo).exclude(Q(id__in=qs) | Q(id_user__in=jefaturas_pefiles))

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
            'jefatura_primerarevision',


        ]

        widgets = {
            'estado_flujo': forms.Select(attrs={'class': 'form-control', 'readonly':'readonly'}),
            'jefatura_primerarevision': forms.Select(attrs={'class': 'form-control'}),
            'id_jefatura': forms.Select(attrs={'class': 'form-control', 'readonly':'readonly'}),
        }
