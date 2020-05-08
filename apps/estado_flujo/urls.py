from django.urls import path
from django.conf.urls import url
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [

    path('listar', login_required(views.EstadoFlujoList.as_view()), name='EstadoFlujo_listar'),
    path('create', login_required(views.EstadoFlujoCreate.as_view()), name='EstadoFlujo_crear'),
    path('edit/<int:pk>', login_required(views.EstadoFlujoEdit.as_view()), name='EstadoFlujo_editar'),
    path('delete/<int:pk>', login_required(views.EstadoFlujoDelete.as_view()), name='EstadoFlujo_delete'),
    ]