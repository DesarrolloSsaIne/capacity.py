from django import forms
from apps.productos.models import Glo_ProductosEstadisticos

class productoForm(forms.ModelForm):

    class Meta:
        model = Glo_ProductosEstadisticos

        fields = [
            'descripcion_producto',


        ]


        widgets = {

            'descripcion_producto': forms.TextInput(attrs={'class': 'form-control'}),

        }

