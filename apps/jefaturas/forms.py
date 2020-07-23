from django import forms
from apps.jefaturas.models import Ges_Jefatura
from apps.estructura.models import Ges_Niveles
from django.contrib.auth.models import User, Group

class JefaturasForm(forms.ModelForm):



    def __init__(self,*args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(JefaturasForm, self).__init__(*args, **kwargs)

        jefes_list=list(Ges_Jefatura.objects.values_list('id_user_id', flat=True))
        self.fields['id_user'].queryset = User.objects.all().exclude(id__in=jefes_list)

        nivel_list=list(Ges_Jefatura.objects.values_list('id_nivel_id', flat=True))
        self.fields['id_nivel'].queryset = Ges_Niveles.objects.all().exclude(id__in=nivel_list)


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


class JefaturasFormUpdate(forms.ModelForm):

    def __init__(self,*args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(JefaturasFormUpdate, self).__init__(*args, **kwargs)
        jefes_list=list(Ges_Jefatura.objects.values_list('id_user_id', flat=True))
        self.fields['id_user'].queryset = User.objects.all().exclude(id__in=jefes_list)


    class Meta:
        model = Ges_Jefatura


        fields = [

            'id_user',
            'id_nivel',




        ]

        widgets = {

            'id_user': forms.Select(attrs={'class': 'form-control', 'id': 'siteID', 'style':'width:550px;'}),

            'id_nivel': forms.Select(attrs={'class': 'form-control', 'id': 'siteID2', 'style':'width:550px;', 'disabled':'true' }),
        }