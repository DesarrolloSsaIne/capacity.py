from django import forms
from apps.objetivos.models import Ges_Objetivo_Estrategico, Ges_Objetivo_Tactico, Ges_Objetivo_Operativo, Ges_Objetivo_TacticoTN



class ObjetivosEstrategicosForm (forms.ModelForm):

    class Meta:
        model = Ges_Objetivo_Estrategico

        fields = [
            'ges_eje',
            'descripcion_objetivo',
             'ges_primer_nivel',

        ]

        widgets = {

            'ges_eje': forms.Select(attrs={'class': 'form-control'}),
            'descripcion_objetivo': forms.TextInput(attrs={'class': 'form-control'}),
             'ges_primer_nivel': forms.Select(attrs={'class': 'form-control'}),
        }


class ObjetivosTacticosForm_sn (forms.ModelForm):

    class Meta:
        model = Ges_Objetivo_Tactico

        fields = [
            'id_objetivo_estrategico',
             'descripcion_objetivo',


        ]

        widgets = {
            'id_objetivo_estrategico': forms.Select(attrs={'class': 'form-control'}),
               'descripcion_objetivo': forms.TextInput(attrs={'class': 'form-control'}),
              #'ges_segundo_nivel': forms.Select(attrs={'class': 'form-control', 'style':'pointer-events: none; background-color:#ecedf0; '}),
        }



class ObjetivosTacticosForm_sn_new (forms.ModelForm):

    class Meta:
        model = Ges_Objetivo_Tactico

        fields = [
            'id_objetivo_estrategico',
             'descripcion_objetivo',


        ]

        widgets = {
               'id_objetivo_estrategico': forms.Select(attrs={'class': 'form-control'}),
               'descripcion_objetivo': forms.TextInput(attrs={'class': 'form-control'}),

        }


class ObjetivosTacticosForm_tn_new (forms.ModelForm):

    #con eso traigo solo los objetivos tácticos
    def __init__(self, id_segundo_nivel, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(ObjetivosTacticosForm_tn_new, self).__init__(*args, **kwargs)
        self.fields['id_objetivo_tactico'].queryset =  Ges_Objetivo_Tactico.objects.filter(id_segundo_nivel=id_segundo_nivel)


    class Meta:
        model = Ges_Objetivo_TacticoTN

        fields = [
            'id_objetivo_tactico',
             'descripcion_objetivo',


        ]

        widgets = {
               'id_objetivo_tactico': forms.Select(attrs={'class': 'form-control'}),
               'descripcion_objetivo': forms.TextInput(attrs={'class': 'form-control'}),

        }


class ObjetivosTacticosFormEdit_tn_new (forms.ModelForm):


    #con eso traigo solo los objetivos tácticos
    def __init__(self, id_segundo_nivel, *args, **kwargs):
        super(ObjetivosTacticosFormEdit_tn_new, self).__init__(*args, **kwargs)
        self.fields['id_objetivo_tactico'].queryset =  Ges_Objetivo_Tactico.objects.filter(id_segundo_nivel=id_segundo_nivel)

    class Meta:
        model = Ges_Objetivo_TacticoTN

        fields = [
            'id_objetivo_tactico',
             'descripcion_objetivo',


        ]

        widgets = {
               'id_objetivo_tactico': forms.Select(attrs={'class': 'form-control'}),
               'descripcion_objetivo': forms.TextInput(attrs={'class': 'form-control'}),

        }


class ObjetivosOperativosForm(forms.ModelForm):

    #con eso traigo solo los objetivos tácticos
    def __init__(self, id_tercer_nivel, *args, **kwargs):
        super(ObjetivosOperativosForm, self).__init__(*args, **kwargs)
        self.fields['id_objetivo_tacticotn'].queryset =  Ges_Objetivo_TacticoTN.objects.filter(id_tercer_nivel=id_tercer_nivel)

    class Meta:
        model = Ges_Objetivo_Operativo

        fields = [
            'id_objetivo_tacticotn',
             'descripcion_objetivo',


        ]

        widgets = {
               'id_objetivo_tacticotn': forms.Select(attrs={'class': 'form-control'}),
               'descripcion_objetivo': forms.TextInput(attrs={'class': 'form-control'}),

        }
