from django import forms
from apps.controlador.models import Ges_Controlador
from django.contrib.auth.models import User, Group


class Planificacion_adminForm(forms.ModelForm):

    def __init__(self,*args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(Planificacion_adminForm, self).__init__(*args, **kwargs)
        self.fields['analista_asignado'].queryset = User.objects.filter(groups__in=Group.objects.filter(id=6))


    class Meta:
        model = Ges_Controlador
        fields = [
            'analista_asignado',

        ]

        widgets = {
            'analista_asignado': forms.Select(attrs={'class': 'form-control',  'id': 'siteID', 'style':'width:550px;'}),

        }
