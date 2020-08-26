from django import forms
from apps.jefaturas.models import Ges_Jefatura
from apps.estructura.models import Ges_Niveles
from apps.registration.models import UsuariosExcepcion
from django.contrib.auth.models import User, Group
from django.db.models import Q
class JefaturasForm(forms.ModelForm):



    def __init__(self,*args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(JefaturasForm, self).__init__(*args, **kwargs)

        jefes_list=list(Ges_Jefatura.objects.values_list('id_user_id', flat=True))
        analistas=list(User.objects.values_list('id', flat=True).filter(groups__in=Group.objects.filter(id='6')))

        cuentas_genericas=list(UsuariosExcepcion.objects.values_list('username', flat=True))
        cuentas_genericas_id = list(User.objects.values_list('id', flat=True).filter(username__in=cuentas_genericas))
        self.fields['id_user'].queryset = User.objects.all().exclude(Q(id__in=analistas) | Q(id__in=jefes_list) | Q(id__in=cuentas_genericas_id) | Q(first_name='geoportal')).order_by('username')

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

        analistas = list(User.objects.values_list('id', flat=True).filter(groups__in=Group.objects.filter(id='6')))
        jefes_list=list(Ges_Jefatura.objects.values_list('id_user_id', flat=True))
        cuentas_genericas = list(UsuariosExcepcion.objects.values_list('username', flat=True))
        cuentas_genericas_id = list(User.objects.values_list('id', flat=True).filter(username__in=cuentas_genericas))
        self.fields['id_user'].queryset = User.objects.all().exclude(
            Q(id__in=analistas) | Q(id__in=jefes_list) | Q(id__in=cuentas_genericas_id) | Q(
                first_name='geoportal')).order_by('username')


    class Meta:
        model = Ges_Jefatura


        fields = [

            'id_user',
            'id_nivel',




        ]

        widgets = {

            'id_user': forms.Select(attrs={'class': 'form-control', 'id': 'siteID', 'style':'width:550px;'}),

            'id_nivel': forms.Select(attrs={'class': 'form-control', 'id': 'siteID2edit', 'style':'width:550px;' }),
        }