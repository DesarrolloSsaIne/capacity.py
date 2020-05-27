from django import forms
from apps.periodos.models import Glo_Periodos, Glo_Seguimiento

class periodosForm(forms.ModelForm):
    ANIO_CHOICES = (
        (2020, '2020'),
        (2021, '2021'),
        (2022, '2022'),
        (2023, '2023'),
        (2024, '2024'),
        (2025, '2025')
    )

    TRUE_FALSE_CHOICES = (
        (True, 'Activo'),
        (False, 'Inactivo')

    )

    anio_periodo = forms.ChoiceField(choices=ANIO_CHOICES,
                                   widget=forms.Select(attrs={'class': 'form-control'}))


    estado = forms.ChoiceField(choices=TRUE_FALSE_CHOICES,
                                   widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Glo_Periodos

        fields = [
            'descripcion_periodo',
            'anio_periodo',
            'estado',

        ]


        widgets = {

            'descripcion_periodo': forms.TextInput(attrs={'class': 'form-control'}),

        }

class Seguimiento_cierreform(forms.ModelForm):


    class Meta:
        model = Glo_Seguimiento
        fields = [
            'fecha_termino',

        ]


