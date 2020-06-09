from django.conf.urls import url, include
from apps.seguimiento_formula.views import ActividadesObjetivosList,ActividadesDetail,ActividadEdit, iniciaSeguimiento,cierraSeguimiento
from django.contrib.auth.decorators import login_required
from django.urls import path

urlpatterns = [

    url(r'listar', login_required(ActividadesObjetivosList.as_view()), name='ActividadesObjetivosListarSeguimiento'),
    url('detalle/(?P<pk>\d+)/', login_required(ActividadesDetail.as_view()),
        name='ActividadesDetailSeguimiento'),

    url('editar/(?P<pk>\d+)/$', login_required(ActividadEdit.as_view()), name='RegistroActividadEditarSeguimiento'),
    path('iniciaEjecucion/<int:pk>', login_required(iniciaSeguimiento.as_view()), name='iniciaEjecucion'),
    path('cierreEjecucion/<int:pk>', login_required(cierraSeguimiento.as_view()), name='cierreEjecucion'),
]