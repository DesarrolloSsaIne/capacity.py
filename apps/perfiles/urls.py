
from django.conf.urls import url, include
from apps.perfiles.views import PerfilesList, PerfilAsigna, PerfilDelete, PerfilUsuarioList, PerfilesListAnalistas, PerfilDeleteAnalista, PerfilAsignaAnalista
from django.contrib.auth.decorators import login_required
from django.urls import path

urlpatterns = [


    # url(r'crear/', login_required(JefaturaCreate.as_view()), name='JefaturaCrear'),
    url(r'listar/', login_required(PerfilesList.as_view()), name='PerfilListar'),
    url(r'listarAnalistas/', login_required(PerfilesListAnalistas.as_view()), name='PerfilListarAnalistas'),
    # url('editar/(?P<pk>\d+)/$', login_required(JefaturaUpdate.as_view()), name='JefaturaEditar'),
    # url('eliminar/(?P<pk>\d+)/$', login_required(AnalistaDelete.as_view()), name='AnalistaEliminar'),
    path('eliminar/<int:id>', login_required(PerfilDelete), name="PerfilEliminar"),

    path('eliminarAnalista/<int:id>', login_required(PerfilDeleteAnalista), name="PerfilEliminarAnalista"),

    url('listarUsuarios/(?P<pk>\d+)/$', login_required(PerfilUsuarioList.as_view()), name="PerfilListarUsuarios"),

    path('crear/', login_required(PerfilAsigna), name="PerfilCrear"),
    path('crearAnalista/', login_required(PerfilAsignaAnalista), name="PerfilCrearAnalista"),
    #url('editar/2/(?P<id_nivel>\d+)/$', SegundoNivelUpdate, name='SegundoNivelEditar'),

]