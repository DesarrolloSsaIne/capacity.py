from django.urls import path
from django.conf.urls import url
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [

    path('listar', login_required(views.ControladorList.as_view()), name='controlador_listar'),
    path('create', login_required(views.ControladorCreate.as_view()), name='controlador_crear'),
    path('edit/<int:pk>', login_required(views.ControladorUpdate.as_view()), name='controlador_editar'),
    path('delete/<int:pk>', login_required(views.ControladorDelete.as_view()), name='controlador_delete'),
]