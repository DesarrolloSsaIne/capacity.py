from django.conf.urls import url, include
from apps.objetivos.views import ObjetivosEstrategicosList, ObjetivosEstrategicosCreate, ObjetivosEstrategicosDelete , \
    ObjetivosEstrategicosEdit , ObjetivosTacticosEdit, ObjetivosTacticosDetail, ObjetivosTacticosDelete, \
    ObjetivosTacticosCreate, ObjetivosTacticosDetailTN, ObjetivosTacticosCreateTN, ObjetivosTacticosEditTN, \
    ObjetivosTacticosDeleteTN, ObjetivosOperativosDetail, ObjetivosOperativosCreate, ObjetivosOperativosEdit, \
    ObjetivosOperativosDelete
from django.contrib.auth.decorators import login_required


urlpatterns = [



    url(r'estrategicos/crear/', login_required(ObjetivosEstrategicosCreate.as_view()), name='ObjetivosEstrategicosCrear'),
    url(r'estrategicos/listar/', login_required(ObjetivosEstrategicosList.as_view()), name='ObjetivosEstrategicosListar'),
    url('estrategicos/editar/(?P<pk>\d+)/$', login_required(ObjetivosEstrategicosEdit.as_view()), name='ObjetivosEstrategicosEdit'),
    url('estrategicos/eliminar/(?P<pk>\d+)/$', login_required(ObjetivosEstrategicosDelete.as_view()), name='ObjetivosEstrategicosDelete'),

    url(r'tacticos/sn/create/', login_required(ObjetivosTacticosCreate.as_view()), name='ObjetivosTacticosCrear'),
  #  url(r'tacticos/sn/list', login_required(ObjetivosTacticosList.as_view()), name='ObjetivosTacticosListar'),
    url('tacticos/sn/detail/(?P<pk>\d+)/', login_required(ObjetivosTacticosDetail.as_view()), name='ObjetivosTacticosDetalle'),
    url('tacticos/sn/edit/(?P<pk>\d+)/$', login_required(ObjetivosTacticosEdit.as_view()), name='ObjetivosTacticosEdit'),
    url('tacticos/sn/delete/(?P<pk>\d+)/$', login_required(ObjetivosTacticosDelete.as_view()), name='ObjetivosTacticosDelete'),

    url('tacticos/tn/detail/(?P<pk>\d+)/', login_required(ObjetivosTacticosDetailTN.as_view()), name='ObjetivosTacticosDetalleTN'),
    url(r'tacticos/tn/create/', login_required(ObjetivosTacticosCreateTN.as_view()), name='ObjetivosTacticosCrearTN'),
    url('tacticos/tn/edit/(?P<pk>\d+)/$', login_required(ObjetivosTacticosEditTN.as_view()), name='ObjetivosTacticosEditTN'),
    url('tacticos/tn/delete/(?P<pk>\d+)/$', login_required(ObjetivosTacticosDeleteTN.as_view()), name='ObjetivosTacticosDeleteTN'),
    #url('editar/2/(?P<id_nivel>\d+)/$', SegundoNivelUpdate, name='SegundoNivelEditar'),

    url('operativos/detail/(?P<pk>\d+)/', login_required(ObjetivosOperativosDetail.as_view()), name='ObjetivosOperativosDetail'),
    url(r'operativos/create/', login_required(ObjetivosOperativosCreate.as_view()), name='ObjetivosOperativosCrear'),
    url('operativos/edit/(?P<pk>\d+)/$', login_required(ObjetivosOperativosEdit.as_view()), name='ObjetivosOperativosEdit'),
    url('operativos/delete/(?P<pk>\d+)/$', login_required(ObjetivosOperativosDelete.as_view()), name='ObjetivosOperativosDelete'),
]

