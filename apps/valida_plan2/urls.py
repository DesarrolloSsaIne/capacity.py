from django.urls import path
from django.conf.urls import url
from . import views
from django.contrib.auth.decorators import login_required
from django.conf.urls import url
from apps.valida_plan2.views import UnidadesList, Objetivos, Actividades,  RechazaPlan, AceptaPlan, \
    ObservacionesListar,GestionObservacionesVer, GestionObservacionesObjetivosVp2, ActividadDetalle

urlpatterns = [

    url(r'listarUnidades2', login_required(UnidadesList.as_view()), name='UnidadesList2'),
    url('listaObjetivosb2/(?P<pk>\d+)/', login_required(Objetivos.as_view()), name='ActividadesDetalles2'),
    url('listarActividadesb2/(?P<pk>\d+)/', login_required(Actividades.as_view()), name='Actividades2'),
    url('listaObservacionb2/(?P<pk>\d+)/', login_required(ObservacionesListar.as_view()), name='observacionesListar2'),
    # url('registraObservacionb2', login_required(ObservacionesCreate.as_view()), name='RegistraObservaciones2'),
    # url('observacionDeleteb2/(?P<pk>\d+)/', login_required(ObservacionDelete.as_view()), name='ObservacionBorrar2'),
    # url('observacionUpdateb2/(?P<pk>\d+)/', login_required(ObservacionUpdate.as_view()), name='ObservacionActualiza2'),

    path('gestionObservacionVer/<int:id>', GestionObservacionesVer, name="gestionobservacionver"),
path('gestionObservacionVp2/<int:id>', GestionObservacionesObjetivosVp2, name="gestionobservacionvp2"),

path('detalleactividadesVp2/<int:id>', ActividadDetalle, name="detalleactividadesValidaPlan2"),

########################################################################################################################
########################################################################################################################
########################################################################################################################

    path('rechazaplanb2/<int:pk>', login_required(RechazaPlan.as_view()), name='rechazaplan2'),
    path('aceptaplanb2/<int:pk>', login_required(AceptaPlan.as_view()), name='aceptaplan2'),
]


