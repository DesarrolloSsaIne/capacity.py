from django.urls import path
from django.conf.urls import url
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url('listar', login_required(views.EjeList.as_view()), name='EjeListar'),
    url('Nuevo', login_required(views.EjeCreate.as_view()), name='EjeCrear'),
    path('Editar/<int:pk>', login_required(views.EjeUpdate.as_view()), name='EjeEditar'),
    path('Eliminar/<int:pk>', login_required(views.EjeDelete.as_view()), name='EjeEliminar'),
]