from django.contrib.auth.decorators import login_required
from django.conf.urls import url
from django.urls import path
from apps.valida_seguimiento.views import UnidadesList, Objetivos, Actividades, ActividadEdit, update_actividad, update_actividad_rechaza, ValidaSeguimientoActividadDetallesVer

urlpatterns = [

    url(r'listarUnidades', login_required(UnidadesList.as_view()), name='UnidadesListValida'),
    url('listaObjetivos/(?P<pk>\d+)/', login_required(Objetivos.as_view()), name='ActividadesDetallesValida'),
    url('listarActividades/(?P<pk>\d+)/', login_required(Actividades.as_view()), name='ActividadesValidar'),
    url('ver/(?P<pk>\d+)/$', login_required(ValidaSeguimientoActividadDetallesVer.as_view()), name='ValidaSeguimientoActividadesVer'),
    url('editar/(?P<pk>\d+)/$', login_required(ActividadEdit.as_view()), name='RegistroActividadEditarSeguimientoValidar'),

    url(r'update_actividad/', update_actividad, name='update_actividad'),
    url(r'update_actividad_rechaza/', update_actividad_rechaza, name='update_actividad_rechaza'),

]
