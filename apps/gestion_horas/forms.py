from django import forms
from apps.gestion_horas.models import Ges_Registro_Horas
import datetime
from django.contrib.auth.models import User
from apps.registration.models import UsuariosExcepcion
from django.contrib.auth.models import User, Group
from django.db.models import Q

class DateInput(forms.DateInput):
    input_type = 'date'

class GestionHorasForm(forms.ModelForm):
    def __init__(self,*args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(GestionHorasForm, self).__init__(*args, **kwargs)


        cuentas_genericas=list(UsuariosExcepcion.objects.values_list('username', flat=True))
        cuentas_genericas_id = list(User.objects.values_list('id', flat=True).filter(username__in=cuentas_genericas))
        self.fields['id_user'].queryset = User.objects.all().exclude(Q(id__in=cuentas_genericas_id) | Q(first_name='geoportal')).order_by('username')


    TRUE_FALSE_CHOICES = (
        (True, 'Si'),
        (False, 'No')
    )
    tiene_vacaciones = forms.ChoiceField(choices=TRUE_FALSE_CHOICES,
                                   widget=forms.Select(attrs={'class': 'form-control'}))





    class Meta:
        model = Ges_Registro_Horas


        fields = [
            'id_familiacargo',
            'id_user',
            'tiene_vacaciones',
            'fecha_inicio',
            'fecha_termino',
            'notas',
        ]

        widgets = {
            'id_familiacargo': forms.Select(attrs={'class':'form-control'}),
            'id_user': forms.Select(attrs={'class': 'form-control','id':'siteID'}),
            'fecha_inicio': DateInput(attrs={'class': 'form-control'}),
            'fecha_termino': DateInput(attrs={'class': 'form-control'}),
            'notas': forms.Textarea(attrs={'class': 'form-control','style':'height:100px;'}),


        }


class GestionHorasUpdateForm(forms.ModelForm):
    def __init__(self,*args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(GestionHorasUpdateForm, self).__init__(*args, **kwargs)


        cuentas_genericas=list(UsuariosExcepcion.objects.values_list('username', flat=True))
        cuentas_genericas_id = list(User.objects.values_list('id', flat=True).filter(username__in=cuentas_genericas))
        self.fields['id_user'].queryset = User.objects.all().exclude(Q(id__in=cuentas_genericas_id) | Q(first_name='geoportal')).order_by('username')

    TRUE_FALSE_CHOICES = (
        (True, 'Si'),
        (False, 'No')
    )
    tiene_vacaciones = forms.ChoiceField(choices=TRUE_FALSE_CHOICES,
                                   widget=forms.Select(attrs={'class': 'form-control'}))

    fecha_inicio = forms.DateField(
        widget=forms.DateInput(format='%Y-%m-%d'),
        input_formats=('%Y-%m-%d',)
    )

    fecha_termino= forms.DateField(
        widget=forms.DateInput(format='%Y-%m-%d'),
        input_formats=('%Y-%m-%d',)
    )



    class Meta:
        model = Ges_Registro_Horas


        fields = [
            'id_familiacargo',
            'id_user',
            'tiene_vacaciones',
            'fecha_inicio',
            'fecha_termino',
            'notas',
        ]

        widgets = {
            'id_familiacargo': forms.Select(attrs={'class':'form-control'}),
            'id_user': forms.Select(attrs={'class': 'form-control','id':'siteID'}),
           # 'fecha_inicio': forms.DateInput(format='%d-%m-%Y', attrs={'class': 'datepicker form-control'}),
            #'fecha_termino': forms.DateInput(format='%d-%m-%Y', attrs={'class': 'datepicker form-control'}),
            'notas': forms.Textarea(attrs={'class': 'form-control','style':'height:100px;'}),


        }
