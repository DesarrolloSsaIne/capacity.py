from django import forms
from apps.valida_plan.models import Ges_Observaciones, Ges_Controlador, Ges_Jefatura
from apps.actividades.models import Ges_Actividad
from django.contrib.auth.models import User
from apps.jefaturas.models import Ges_Jefatura as Gj



class RechazaPlanUpdateForm(forms.ModelForm):

    class Meta:
        model = Ges_Controlador

        fields = [
            'estado_flujo',
          #  'jefatura_segundarevision'
        ]

        widgets = {

            'estado_flujo': forms.TextInput(attrs={'class': 'form-control'}),
           # 'jefatura_segundarevision': forms.TextInput(attrs={'class': 'form-control'}),
        }

#############################################################################################################
#############################################################################################################
#############################################################################################################


class ValidaPlanObservacionesForm(forms.ModelForm):

    class Meta:
        model = Ges_Observaciones

        fields = [
            'observacion',

        ]
        widgets = {

            'observacion': forms.Textarea(attrs={'class': 'form-control' , 'style':'width:535px; '}),

        }


class ObservacionForm(forms.ModelForm): #Class agregada por JR - OK
    def __init__(self, id_user, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(ObservacionForm, self).__init__(*args, **kwargs)
        self.fields['user_observa'].queryset = User.objects.filter(id=id_user)


    class Meta:
        model = Ges_Observaciones

        fields = [
            'fecha_registro',
            'user_observa',
            'observacion',

        ]
        widgets = {

             'fecha_registro': forms.DateTimeInput(attrs={'class': 'form-control','style':'width:535px;','readonly':'True'}),
             'user_observa': forms.Select(attrs={'class': 'form-control','style':'width:535px;','readonly':'True'}),
             'observacion': forms.Textarea(attrs={'class': 'form-control' , 'style':'width:535px;','readonly':'True'}),

        }

class ValidaPlanUpdateForm(forms.ModelForm):

    def __init__(self,nivel_jefatura ,*args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(ValidaPlanUpdateForm, self).__init__(*args, **kwargs)
        self.fields['jefatura_segundarevision'].queryset = Gj.objects.filter(id_nivel_id=nivel_jefatura)

    class Meta:
        model = Ges_Controlador
        fields = [
            'estado_flujo',
            'id_jefatura',
            'jefatura_segundarevision'

        ]

        widgets = {
            'estado_flujo': forms.Select(attrs={'class': 'form-control', 'readonly':'readonly'}),
            'jefatura_segundarevision': forms.Select(attrs={'class': 'form-control'}),
            'id_jefatura': forms.Select(attrs={'class': 'form-control', 'readonly':'readonly'}),
        }


class Valida_plan_DetalleForm(forms.ModelForm):

    class Meta:
        model = Ges_Actividad
        fields = [

            'id_periodicidad',
            'horas_actividad',
            'volumen',
            'personas_asignadas',
            'total_horas',
            'id_producto_estadistico',
            'id_estado_actividad',


        ]

        widgets = {

            'id_producto_estadistico': forms.Select(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'id_periodicidad': forms.Select(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'horas_actividad': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'volumen': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'personas_asignadas': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'total_horas': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'id_estado_actividad': forms.Select(attrs={'class': 'form-control'}),


        }
