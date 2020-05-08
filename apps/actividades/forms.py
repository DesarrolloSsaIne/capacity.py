from django import forms
from apps.actividades.models import Ges_Actividad
from apps.familia_cargo.models import Glo_FamiliaCargo as Fc
from apps.controlador.models import Ges_Controlador as Gc
from apps.jefaturas.models import Ges_Jefatura as Gj
from django.db.models import Subquery
class DateInput(forms.DateInput):
    input_type = 'date'


class ActividadForm(forms.ModelForm):
    # con eso traigo solo los objetivos tácticos
    def __init__(self, transversal, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(ActividadForm, self).__init__(*args, **kwargs)
        if transversal == True:
            self.fields['id_familia_cargo'].queryset = Fc.objects.filter(id__in=[2, 3])
        else:
            self.fields['id_familia_cargo'].queryset = Fc.objects.all()

    class Meta:
        model = Ges_Actividad

        fields = [
            'descripcion_actividad',
            'id_periodicidad',
            'horas_actividad',
            'volumen',
            'personas_asignadas',
            'id_familia_cargo',
            'id_producto_estadistico',
            'fecha_inicio_actividad',
            'fecha_termino_actividad',
            'total_horas',
        ]

        widgets = {

            'descripcion_actividad': forms.Textarea(attrs={'class': 'form-control', 'style':'height:80px;'}),
            'id_periodicidad': forms.Select(attrs={'class': 'form-control'}),
             'id_producto_estadistico': forms.Select(attrs={'class': 'form-control'}),
            'horas_actividad': forms.TextInput(attrs={'class': 'form-control', 'id':'horas_actividad_id'}),
            'volumen': forms.TextInput(attrs={'class': 'form-control' , 'id':'volumen_id'}),
            'personas_asignadas': forms.TextInput(attrs={'class': 'form-control' , 'id':'personas_asignadas_id'}),
            'total_horas': forms.TextInput(attrs={'class': 'form-control', 'id': 'total_horas_id', 'readonly':'readonly'}),
            'id_familia_cargo': forms.Select(attrs={'class': 'form-control'}),
            'fecha_inicio_actividad': DateInput(attrs={'class': 'form-control', 'id':'fecha_inicio_actividad'}),
            'fecha_termino_actividad': DateInput(attrs={'class': 'form-control', 'id':'fecha_termino_actividad'}),
        }
class GestionActividadesUpdateForm(forms.ModelForm):

    fecha_inicio_actividad = forms.DateField(
        widget=forms.DateInput(format='%Y-%m-%d'),
        input_formats=('%Y-%m-%d',)
    )

    fecha_termino_actividad= forms.DateField(
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
            'id_familia_cargo',
            'id_producto_estadistico',
            'fecha_inicio_actividad',
            'fecha_termino_actividad',
            'total_horas',
        ]

        widgets = {
            'descripcion_actividad': forms.Textarea(attrs={'class': 'form-control', 'style': 'height:80px;'}),
            'id_periodicidad': forms.Select(attrs={'class': 'form-control'}),
            'id_producto_estadistico': forms.Select(attrs={'class': 'form-control'}),
            'horas_actividad': forms.TextInput(attrs={'class': 'form-control', 'id': 'horas_actividad_id'}),
            'volumen': forms.TextInput(attrs={'class': 'form-control', 'id': 'volumen_id'}),
            'personas_asignadas': forms.TextInput(attrs={'class': 'form-control', 'id': 'personas_asignadas_id'}),
            'total_horas': forms.TextInput(attrs={'class': 'form-control', 'id': 'total_horas_id', 'readonly':'readonly'}),
            'id_familia_cargo': forms.Select(attrs={'class': 'form-control'}),
            #'fecha_inicio_actividad': DateInput(attrs={'class': 'form-control'}),
            #'fecha_termino_actividad': DateInput(attrs={'class': 'form-control'}),
        }





