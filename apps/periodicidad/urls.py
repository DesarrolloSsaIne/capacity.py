from django.urls import path
from django.conf.urls import url
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [

    path('listar', login_required(views.PeriodicidadList.as_view()), name='periodicidad_listar'),
    path('create', login_required(views.PeriodicidadCreate.as_view()), name='periodicidad_crear'),
    path('edit/<int:pk>', login_required(views.PeriodicidadEdit.as_view()), name='periodicidad_editar'),
    path('delete/<int:pk>', login_required(views.PeriodicidadDelete.as_view()), name='periodicidad_delete'),
]