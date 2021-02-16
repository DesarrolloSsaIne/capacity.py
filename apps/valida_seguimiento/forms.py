from django import forms
from apps.actividades.models import Ges_Actividad
from apps.controlador.models import Ges_Controlador
from apps.estado_actividad.models import Glo_EstadoActividad


class ValidaActividadesUpdateForm(forms.ModelForm):

    def __init__(self,id_estado_actual, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(ValidaActividadesUpdateForm, self).__init__(*args, **kwargs)
        self.fields['id_estado_actividad'].queryset = Glo_EstadoActividad.objects.filter(id__in=[id_estado_actual ])



        # asi vuelves tus campos no requeridos
        for key in self.fields:
            self.fields[key].required = False


    fecha_inicio_actividad = forms.DateField(
        widget=forms.DateInput(format='%Y-%m-%d'),
        input_formats=('%Y-%m-%d',)
    )

    fecha_termino_actividad= forms.DateField(
        widget=forms.DateInput(format='%Y-%m-%d'),
        input_formats=('%Y-%m-%d',)
    )

    fecha_real_inicio = forms.DateField(
        widget=forms.DateInput(format='%Y-%m-%d'),
        input_formats=('%Y-%m-%d',)
    )

    fecha_real_termino = forms.DateField(
        widget=forms.DateInput(format='%Y-%m-%d'),
        input_formats=('%Y-%m-%d',)
    )

    fecha_reprogramacion_inicio = forms.DateField(
        widget=forms.DateInput(format='%Y-%m-%d'),
        input_formats=('%Y-%m-%d',)
    )
    fecha_reprogramacion_termino = forms.DateField(
        widget=forms.DateInput(format='%Y-%m-%d'),
        input_formats=('%Y-%m-%d',)
    )


    class Meta:
        model = Ges_Actividad
        fields = [
            'descripcion_actividad',
            'id_periodicidad',
            'horas_actividad',
            'volumen',
            'personas_asignadas',
            'total_horas',
            'id_producto_estadistico',
            'fecha_inicio_actividad',
            'fecha_termino_actividad',
            'fecha_real_termino',
            'fecha_real_inicio',
            'id_estado_actividad',
            'fecha_reprogramacion_inicio',
            'fecha_reprogramacion_termino',
            'justificacion',


        ]

        widgets = {

            'descripcion_actividad': forms.Textarea(attrs={'class': 'form-control', 'style': 'height:80px;', 'readonly': 'readonly'}),
            'id_producto_estadistico': forms.Select(attrs={'class': 'form-control', 'readonly':'readonly'}),
            'id_periodicidad': forms.Select(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'horas_actividad': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'volumen': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'personas_asignadas': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'total_horas': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'id_estado_actividad': forms.Select(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'justificacion': forms.Textarea(attrs={'class': 'form-control', 'style': 'height:80px;', 'readonly': 'readonly'}),


        }

        outputs = {

            '': None
        }

class ValidaSeguimientoUpdateFormVer(forms.ModelForm):




    fecha_inicio_actividad = forms.DateField(
        widget=forms.DateInput(format='%Y-%m-%d'),
        input_formats=('%Y-%m-%d',)
    )

    fecha_termino_actividad= forms.DateField(
        widget=forms.DateInput(format='%Y-%m-%d'),
        input_formats=('%Y-%m-%d',)
    )

    fecha_real_inicio = forms.DateField(
        widget=forms.DateInput(format='%Y-%m-%d'),
        input_formats=('%Y-%m-%d',)
    )

    fecha_real_termino = forms.DateField(
        widget=forms.DateInput(format='%Y-%m-%d'),
        input_formats=('%Y-%m-%d',)
    )

    fecha_reprogramacion_inicio = forms.DateField(
        widget=forms.DateInput(format='%Y-%m-%d'),
        input_formats=('%Y-%m-%d',)
    )
    fecha_reprogramacion_termino = forms.DateField(
        widget=forms.DateInput(format='%Y-%m-%d'),
        input_formats=('%Y-%m-%d',)
    )


    class Meta:
        model = Ges_Actividad
        fields = [
            'descripcion_actividad',
            'id_periodicidad',
            'horas_actividad',
            'volumen',
            'personas_asignadas',
            'total_horas',


            'justificacion',

        ]

        widgets = {

            'descripcion_actividad': forms.Textarea(attrs={'class': 'form-control', 'style': 'height:80px;', 'readonly': 'readonly'}),
            'id_producto_estadistico': forms.Select(attrs={'class': 'form-control', 'readonly':'readonly'}),
            'id_periodicidad': forms.Select(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'horas_actividad': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'volumen': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'personas_asignadas': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'total_horas': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'justificacion': forms.Textarea(attrs={'class': 'form-control', 'style': 'height:80px;' , 'readonly': 'readonly'}),




        }

        outputs = {

            '': None
        }





class PlanUpdateForm(forms.ModelForm):

    class Meta:
        model = Ges_Controlador

        fields = [
            'estado_flujo',
        ]


        widgets = {

            'estado_flujo': forms.TextInput(attrs={'class': 'form-control'}),

        }