from django.contrib.auth.decorators import login_required
from django.conf.urls import url
from django.urls import path
from apps.revision_planificacion.views import UnidadesListar, ObjetivosListar, ActividadesListar, RechazaPlan, AceptaPlan, GestionObservacionesActividades, GestionObservacionesObjetivosVp2

urlpatterns = [

    url(r'listarUnidadesAnalista', login_required(UnidadesListar.as_view()), name='listarUnidadesAnalista'),
    url('listaObjetivosAnalista/(?P<pk>\d+)/', login_required(ObjetivosListar.as_view()), name='listaObjetivosAnalista'),
    url('listarActividadesAnalista/(?P<pk>\d+)/', login_required(ActividadesListar.as_view()), name='listarActividadesAnalista'),
    path('gestionObservacionActividadesA/<int:id>', GestionObservacionesActividades,
         name="gestionobservacionactividadesA"),
path('gestionObservacionAn/<int:id>', GestionObservacionesObjetivosVp2, name="gestionobservacionan"),
    path('rechazaplanAnalista/<int:pk>', login_required(RechazaPlan.as_view()), name='rechazaplanAnalista'),
    path('aceptaplanAnalista/<int:pk>', login_required(AceptaPlan.as_view()), name='aceptaplanAnalista'),
]