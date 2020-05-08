from django import forms
from apps.gestion_horas.models import Ges_Registro_Horas
import datetime
from django.contrib.auth.models import User

class DateInput(forms.DateInput):
    input_type = 'date'

class GestionHorasForm(forms.ModelForm):
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
            'notas': forms.Textarea(attrs={'class': 'form-control', 'style':'width:550px;'}),


        }


class GestionHorasUpdateForm(forms.ModelForm):
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
            'notas': forms.Textarea(attrs={'class': 'form-control','style':'width:550px;'}),


        }
