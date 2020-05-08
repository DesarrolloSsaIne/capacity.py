from django.urls import path
from django.conf.urls import url
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [

    path('listar', login_required(views.PeriodosList.as_view()), name='periodos_listar'),
    path('create', login_required(views.PeriodosCreate.as_view()), name='periodos_crear'),
    path('edit/<int:pk>', login_required(views.PeriodosEdit.as_view()), name='periodo_editar'),
    path('delete/<int:pk>', login_required(views.PeriodosDelete.as_view()), name='periodo_delete'),
]