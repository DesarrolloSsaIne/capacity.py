from django.conf.urls import url, include
from apps.seguimiento_formula.views import ActividadesObjetivosList,ActividadesDetail,ActividadEdit, iniciaSeguimiento,\
    cierraSeguimiento, export_users_xls_seguimiento, ActividadDetallesVer, ObservacionesListar, export_users_xls_seguimiento_comentarios
from django.contrib.auth.decorators import login_required
from django.urls import path

urlpatterns = [

    url(r'listar', login_required(ActividadesObjetivosList.as_view()), name='ActividadesObjetivosListarSeguimiento'),
    url('detalle/(?P<pk>\d+)/', login_required(ActividadesDetail.as_view()),
        name='ActividadesDetailSeguimiento'),

    url('editar/(?P<pk>\d+)/$', login_required(ActividadEdit.as_view()), name='RegistroActividadEditarSeguimiento'),
    url('Observaciones/(?P<pk>\d+)/$', login_required(ObservacionesListar.as_view()), name='ListarObservacionesActividad'),

    url('ver/(?P<pk>\d+)/$', login_required(ActividadDetallesVer.as_view()), name='SeguimientoActividadesVer'),
    path('iniciaEjecucion/<int:pk>', login_required(iniciaSeguimiento.as_view()), name='iniciaEjecucion'),
    path('cierreEjecucion/<int:pk>', login_required(cierraSeguimiento.as_view()), name='cierreEjecucion'),

    path(r'ExportarPlanXlsSeguimiento/<int:pk>', export_users_xls_seguimiento, name='exporta_plan_seguimiento_xls'),
    path(r'DescargarPlanXlsSeguimiento/<int:pk>', export_users_xls_seguimiento_comentarios, name='exporta_plan_seguimiento_xls_comentarios'),

]