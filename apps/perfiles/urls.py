
from django.conf.urls import url, include
from apps.perfiles.views import PerfilesList, PerfilAsigna, PerfilDelete, PerfilUsuarioList
from django.contrib.auth.decorators import login_required
from django.urls import path

urlpatterns = [


    # url(r'crear/', login_required(JefaturaCreate.as_view()), name='JefaturaCrear'),
    url(r'listar/', login_required(PerfilesList.as_view()), name='PerfilListar'),
    # url('editar/(?P<pk>\d+)/$', login_required(JefaturaUpdate.as_view()), name='JefaturaEditar'),
    # url('eliminar/(?P<pk>\d+)/$', login_required(AnalistaDelete.as_view()), name='AnalistaEliminar'),
    path('eliminar/<int:id>', login_required(PerfilDelete), name="PerfilEliminar"),
    path('listarUsuarios/<int:id>', login_required(PerfilUsuarioList), name="PerfilListarUsuarios"),
    path('crear/', login_required(PerfilAsigna), name="PerfilCrear"),
    #url('editar/2/(?P<id_nivel>\d+)/$', SegundoNivelUpdate, name='SegundoNivelEditar'),

]