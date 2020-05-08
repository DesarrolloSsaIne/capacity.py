from django import forms
from apps.valida_plan2.models import  Ges_Controlador
from django.contrib.auth.models import User


class PlanUpdateForm(forms.ModelForm):

    class Meta:
        model = Ges_Controlador

        fields = [
            'estado_flujo',
        ]


        widgets = {

            'estado_flujo': forms.TextInput(attrs={'class': 'form-control'}),

        }





#############################################################################################################
#############################################################################################################
#############################################################################################################


#class ValidaPlanObservacionesForm(forms.ModelForm):

    #class Meta:
        #    model = Ges_Observaciones

        #fields = [
        #   'observacion',

        #]
        #widgets = {

        #    'observacion': forms.Textarea(attrs={'class': 'form-control' , 'style':'width:535px; '}),

        #}

#
# class ObservacionForm(forms.ModelForm): #Class agregada por JR - OK
#     def __init__(self, id_user, *args, **kwargs):
#         self.request = kwargs.pop('request', None)
#         super(ObservacionForm, self).__init__(*args, **kwargs)
#         self.fields['user_observa'].queryset = User.objects.filter(id=id_user)
#
#
#     class Meta:
#         model = Ges_Observaciones
#
#         fields = [
#             'fecha_registro',
#             'user_observa',
#             'observacion',
#
#         ]
#         widgets = {
#
#              'fecha_registro': forms.DateTimeInput(attrs={'class': 'form-control','style':'width:535px;','readonly':'True'}),
#              'user_observa': forms.Select(attrs={'class': 'form-control','style':'width:535px;','readonly':'True'}),
#              'observacion': forms.Textarea(attrs={'class': 'form-control' , 'style':'width:535px;','readonly':'True'}),
#
#         }