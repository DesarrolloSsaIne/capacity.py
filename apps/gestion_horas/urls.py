from django.conf.urls import url, include
from apps.gestion_horas.views import RegistroHorasList, RegistroHorasCreate, RegistroHorasDelete, RegistroHorasUpdate, RegistroHorasDetalle
from django.contrib.auth.decorators import login_required

urlpatterns = [

    url(r'listar/', login_required(RegistroHorasList.as_view()), name='RegistroHorasListar'),
    url(r'detalle/', login_required(RegistroHorasDetalle.as_view()), name='RegistroHorasDetalle'),
    url(r'crear/', login_required(RegistroHorasCreate.as_view()), name='RegistroHorasCrear'),
    url('editar/(?P<pk>\d+)/$', login_required(RegistroHorasUpdate.as_view()), name='RegistroHorasEditar'),
    url('eliminar/(?P<pk>\d+)/$', login_required(RegistroHorasDelete.as_view()), name='RegistroHorasEliminar'),


    ]

