
from django.conf.urls import url, include
from apps.jefaturas.views import JefaturaList, JefaturaCreate, JefaturaDelete, JefaturaUpdate
from django.contrib.auth.decorators import login_required


urlpatterns = [


    url(r'crear/', login_required(JefaturaCreate.as_view()), name='JefaturaCrear'),
    url(r'listar/', login_required(JefaturaList.as_view()), name='JefaturaListar'),
    url('editar/(?P<pk>\d+)/$', login_required(JefaturaUpdate.as_view()), name='JefaturaEditar'),
    url('eliminar/(?P<pk>\d+)/$', login_required(JefaturaDelete.as_view()), name='JefaturaEliminar'),

    #url('editar/2/(?P<id_nivel>\d+)/$', SegundoNivelUpdate, name='SegundoNivelEditar'),

]