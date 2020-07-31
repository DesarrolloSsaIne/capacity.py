from django.urls import path
from django.conf.urls import url
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [

    path('listar', login_required(views.PeriodosList.as_view()), name='periodos_listar'),
    path('create', login_required(views.PeriodosCreate.as_view()), name='periodos_crear'),
    path('edit/<int:pk>', login_required(views.PeriodosEdit.as_view()), name='periodo_editar'),
    path('delete/<int:pk>', login_required(views.PeriodosDelete.as_view()), name='periodo_delete'),

    path('listar_seguimiento/<int:pk>', login_required(views.SeguimientoList.as_view()), name='seguimiento_listar'),
    path('seguimiento_cerrar/<int:pk>', login_required(views.SeguimientoCerrarPeriodo.as_view()), name='seguimiento_cerrar'),
    path('seguimiento_abrir_periodo', login_required(views.SeguimientoAbrirPeriodo.as_view()), name='seguimiento_abrir'),

    path('listar_validacion/<int:pk>', login_required(views.ValidacionList.as_view()), name='validacion_listar'),
    path('validacion_abrir_periodo', login_required(views.ValidacionAbrirPeriodo.as_view()), name='validacion_abrir'),
    path('validacion_cerrar/<int:pk>', login_required(views.ValidacionCerrarPeriodo.as_view()), name='validacion_cerrar'),
]