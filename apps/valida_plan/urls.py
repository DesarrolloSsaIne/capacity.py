from django.urls import path
from django.conf.urls import url
from . import views
from django.contrib.auth.decorators import login_required
from django.conf.urls import url
from apps.valida_plan.views import UnidadesList, Objetivos, Actividades, ObservacionesListar, ObservacionesCreate\
    , ObservacionDelete,  RechazaPlan, AceptaPlan, GestionObservacionesActividades, GestionObservacionesObjetivosVp\
    , SeguimientoUnidadesList, SeguimientoObjetivos, SeguimientoActividades, ActividadDetalle, export_users_xls

urlpatterns = [

    url(r'listarUnidades', login_required(UnidadesList.as_view()), name='UnidadesList'),
    url('listaObjetivos/(?P<pk>\d+)/', login_required(Objetivos.as_view()), name='ActividadesDetalles'),
    url('listarActividades/(?P<pk>\d+)/', login_required(Actividades.as_view()), name='Actividades'),
    url('listaObservacion/(?P<pk>\d+)/', login_required(ObservacionesListar.as_view()), name='observacionesListar'),
    url('registraObservacion', login_required(ObservacionesCreate.as_view()), name='RegistraObservaciones'),
    url('observacionDelete/(?P<pk>\d+)/', login_required(ObservacionDelete.as_view()), name='ObservacionBorrar'),


    path('gestionObservacionActividadesVP/<int:id>', GestionObservacionesActividades, name="gestionobservacionactividadesvp"),
    path('gestionObservacionVp/<int:id>', GestionObservacionesObjetivosVp, name="gestionobservacionvp"),
    path('detalleactividadesVp/<int:id>', ActividadDetalle, name="detalleactividadesvp"),

    path('seguimientoListUnidades', login_required(SeguimientoUnidadesList.as_view()), name='SeguimientoUnidadesList'),
    url('seguimientoListObjetivos/(?P<pk>\d+)/', login_required(SeguimientoObjetivos.as_view()), name='SeguimientoObjetivosList'),
    url('seguimientoListActividades/(?P<pk>\d+)/', login_required(SeguimientoActividades.as_view()), name='SeguimientoActividadesList'),
    path(r'ExportarPlanesXls/<int:pk>', export_users_xls, name='exporta_plan_jefatura_directa_xls'),


########################################################################################################################
########################################################################################################################
########################################################################################################################

    path('rechazaplan/<int:pk>', login_required(RechazaPlan.as_view()), name='rechazaplan'),
    path('aceptaplan/<int:pk>', login_required(AceptaPlan.as_view()), name='aceptaplan'),
]


