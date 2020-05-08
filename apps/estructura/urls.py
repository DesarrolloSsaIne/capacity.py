from django.urls import path, include
from django.conf.urls import url, include
from apps.estructura.views import PrimerNivelList, PrimerNivelUpdate, SegundoNivelList, SegundoNivelUpdate, \
    SegundoNivelCreate, SegundoNivelDelete, TercerNivelCreate, TercerNivelUpdate, TercerNivelList, TercerNivelDelete, \
    CuartoNivelList, CuartoNivelCreate, CuartoNivelUpdate, CuartoNivelDelete
from django.contrib.auth.decorators import login_required

urlpatterns = [

   # url(r'listar', primernivel_list, name='PrimerNivelListar'),
    url('listar/1', login_required(PrimerNivelList.as_view()), name='PrimerNivelListar'),
    url('editar/1/(?P<pk>\d+)/$', login_required(PrimerNivelUpdate.as_view()), name='PrimerNivelEditar'),

    url(r'crear/2', login_required(SegundoNivelCreate.as_view()), name='SegundoNivelCrear'),
    url(r'listar/2', login_required(SegundoNivelList.as_view()), name='SegundoNivelListar'),
    url('editar/2/(?P<pk>\d+)/$', login_required(SegundoNivelUpdate.as_view()), name='SegundoNivelEditar'),
    url('eliminar/2/(?P<pk>\d+)/$', login_required(SegundoNivelDelete.as_view()), name='SegundoNivelDelete'),

    url(r'crear/3', login_required(TercerNivelCreate.as_view()), name='TercerNivelCrear'),
    url(r'listar/3', login_required(TercerNivelList.as_view()), name='TercerNivelListar'),
    url('editar/3/(?P<pk>\d+)/$', login_required(TercerNivelUpdate.as_view()), name='TercerNivelEditar'),
    url('eliminar/3/(?P<pk>\d+)/$', login_required(TercerNivelDelete.as_view()), name='TercerNivelDelete'),

    url(r'crear/4', login_required(CuartoNivelCreate.as_view()), name='CuartoNivelCrear'),
    url(r'listar/4', login_required(CuartoNivelList.as_view()), name='CuartoNivelListar'),
    url('editar/4/(?P<pk>\d+)/$', login_required(CuartoNivelUpdate.as_view()), name='CuartoNivelEditar'),
    url('eliminar/4/(?P<pk>\d+)/$', login_required(CuartoNivelDelete.as_view()), name='CuartoNivelDelete'),

    #url('editar/2/(?P<id_nivel>\d+)/$', SegundoNivelUpdate, name='SegundoNivelEditar'),

]