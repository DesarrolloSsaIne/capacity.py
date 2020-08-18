from django.contrib.auth.decorators import login_required
from django.conf.urls import url
from django.urls import path
from apps.revision_planificacion.views import UnidadesListar, ObjetivosListar, ActividadesListar,\
    RechazaPlan, AceptaPlan, GestionObservacionesActividades, \
    GestionObservacionesObjetivosVp2,ActividadDetalle, UnidadesListarNoFinalizadas, \
    ActividadesListarNoFinalizadas, ObjetivosListarNoFinalizadas, EnviarPlanAdministrador, export_users_xls


urlpatterns = [

    url(r'listarUnidadesAnalista', login_required(UnidadesListar.as_view()), name='listarUnidadesAnalista'),
    url(r'listarUnidadesNoFinalizadas', login_required(UnidadesListarNoFinalizadas.as_view()), name='listarUnidadesNoFin'),


    url('listaObjetivosAnalista/(?P<pk>\d+)/', login_required(ObjetivosListar.as_view()), name='listaObjetivosAnalista'),
    url('listaObjetivosNoFinalizadas/(?P<pk>\d+)/', login_required(ObjetivosListarNoFinalizadas.as_view()), name='listaObjetivosNoFinalizadas'),

    url('listarActividadesAnalista/(?P<pk>\d+)/', login_required(ActividadesListar.as_view()), name='listarActividadesAnalista'),
    url('listarActividadesNoFinalizadas/(?P<pk>\d+)/', login_required(ActividadesListarNoFinalizadas.as_view()), name='listarActividadesNoFina'),

    path('gestionObservacionActividadesA/<int:id>', GestionObservacionesActividades,
         name="gestionobservacionactividadesA"),

    path('detalleactividadesRp/<int:id>', ActividadDetalle, name="detalleactividadesrevisionplanificacion"),

    path('gestionObservacionAn/<int:id>', GestionObservacionesObjetivosVp2, name="gestionobservacionan"),
    path('rechazaplanAnalista/<int:pk>', login_required(RechazaPlan.as_view()), name='rechazaplanAnalista'),
    path('aceptaplanAnalista/<int:pk>', login_required(AceptaPlan.as_view()), name='aceptaplanAnalista'),

    path('enviaplanadministrador/<int:pk>', login_required(EnviarPlanAdministrador.as_view()), name='enviaAdministrador'),

    path(r'ExportarPlanXls/<int:pk>', export_users_xls, name='exporta_plan_analista_xls'),



]