from django import forms
from apps.estructura.models import Ges_PrimerNivel, Ges_SegundoNivel, Ges_TercerNivel, Ges_CuartoNivel
from apps.objetivos.models import Ges_Objetivo_Estrategico
from django.contrib.auth.models import User

class PrimerNivelForm(forms.ModelForm):


    class Meta:
        model = Ges_PrimerNivel

        fields = [
            'descripcion_nivel',

        ]

        widgets = {
            'descripcion_nivel': forms.TextInput(attrs={'class':'form-control'}),


        }


class SegundoNivelForm(forms.ModelForm):


    class Meta:
        model = Ges_SegundoNivel

        fields = [
            'primer_nivel',
            'descripcion_nivel',

            'estado',

        ]

        widgets = {
            'primer_nivel': forms.Select(attrs={'class': 'form-control'}),
            'descripcion_nivel': forms.TextInput(attrs={'class':'form-control'}),


          'estado': forms.CheckboxInput(attrs={'class': 'form-control', 'checked':'true'}),


        }



class TercerNivelForm(forms.ModelForm):

    class Meta:
        model = Ges_TercerNivel

        fields = [
            'segundo_nivel',
            'descripcion_nivel',


            'estado',

        ]

        widgets = {
            'segundo_nivel': forms.Select(attrs={'class': 'form-control'}),
            'descripcion_nivel': forms.TextInput(attrs={'class':'form-control'}),


            'estado': forms.CheckboxInput(attrs={'class': 'form-control', 'checked':'true'}),


        }




class CuartoNivelForm(forms.ModelForm):
    # TRUE_FALSE_CHOICES = (
    #     (True, 'Si'),
    #     (False, 'No')
    # )
    # define_actividad = forms.ChoiceField(choices=TRUE_FALSE_CHOICES,
    #                                widget=forms.Select(attrs={'class': 'form-control'}))
    class Meta:
        model = Ges_CuartoNivel

        fields = [
            'tercer_nivel',
            'descripcion_nivel',


            'estado',

        ]

        widgets = {
            'tercer_nivel': forms.Select(attrs={'class': 'form-control'}),
            'descripcion_nivel': forms.TextInput(attrs={'class':'form-control'}),


            'estado': forms.CheckboxInput(attrs={'class': 'form-control', 'checked':'true'}),


        }

   # def __init__(self, *args, **kwargs):
    #    super(SegundoNivelForm, self).__init__(*args, **kwargs)
     #   self.fields['estado'].initial= True

#'style':'pointer-events: none;' sirve para bloquear un control.
