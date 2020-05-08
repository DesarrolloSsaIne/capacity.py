from django import forms
from apps.feriados.models import Ges_Feriados

class feriadosForm(forms.ModelForm):
    TRUE_FALSE_CHOICES = (
        (2020, '2020'),
        (2021, '2021'),
        (2022, '2022'),
        (2023, '2023'),
        (2024, '2024'),
        (2025, '2025')
    )
    anio_feriado = forms.ChoiceField(choices=TRUE_FALSE_CHOICES,
                                   widget=forms.Select(attrs={'class': 'form-control'}))
    fecha_feriado= forms.DateField(
        widget=forms.DateInput(format='%Y-%m-%d'),
        input_formats=('%Y-%m-%d',)
    )


    class Meta:
        model = Ges_Feriados

        fields = [
            'anio_feriado',
            'fecha_feriado',
            'descripcion_feriado',


        ]
        labels = {
            'anio_feriado': 'Año',
            'fecha_feriado': 'Fecha',
            'descripcion_feriado': 'Descripción',

        }

        widgets = {
          #  'anio_feriado': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion_feriado': forms.TextInput(attrs={'class': 'form-control'}),

        }


