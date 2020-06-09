from django import forms
from apps.actividades.models import Ges_Actividad
from apps.controlador.models import Ges_Controlador


class GestionActividadesUpdateForm(forms.ModelForm):

    def __init__(self,  *args, **kwargs):
        super(GestionActividadesUpdateForm, self).__init__(*args, **kwargs)
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
            'id_producto_estadistico',
            'fecha_inicio_actividad',
            'fecha_termino_actividad',
            'id_estado_actividad',
            'fecha_real_termino',
            'fecha_reprogramacion_inicio',
            'fecha_reprogramacion_termino',
            'justificacion',

        ]

        widgets = {
            'descripcion_actividad': forms.TextInput(attrs={'class': 'form-control', 'readonly':'readonly'}),
            'id_producto_estadistico': forms.Select(attrs={'class': 'form-control', 'readonly':'readonly'}),
            'id_estado_actividad': forms.Select(attrs={'class': 'form-control'}),
            'justificacion': forms.Textarea(attrs={'class': 'form-control', 'style': 'height:80px;'}),

            #'fecha_inicio_actividad': DateInput(attrs={'class': 'form-control'}),
            #'fecha_termino_actividad': DateInput(attrs={'class': 'form-control'}),
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




