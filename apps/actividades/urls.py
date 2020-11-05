from django.conf.urls import url, include
from apps.actividades.views import ActividadesObjetivosList,ActividadesDetail,ActividadCreate, ActividadesDelete,\
    ActividadEdit,update_estate, GestionObservacionesObjetivos,GestionObservacionesActividades, calculaferiados, nuevaActividadAjax ,CalcularFeriados
from django.contrib.auth.decorators import login_required
from django.urls import path

urlpatterns = [

    url(r'listar', login_required(ActividadesObjetivosList.as_view()), name='ActividadesObjetivosListar'),
    url('detalle/(?P<pk>\d+)/', login_required(ActividadesDetail.as_view()),
        name='ActividadesDetail'),

    url(r'crear', login_required(ActividadCreate.as_view()), name='ActividadesCrear'),
    url('editar/(?P<pk>\d+)/$', login_required(ActividadEdit.as_view()), name='RegistroActividadEditar'),
    url('eliminar/(?P<pk>\d+)/$', login_required(ActividadesDelete.as_view()), name='RegistroActividadesEliminar'),

    url(r'^updateEstate/', update_estate, name='updateEstate'),
    url(r'^calculaferiados/', calculaferiados, name='calculaferiados'),
    url(r'^calculaferiadoscreate/', CalcularFeriados, name='calculaferiadoscreate'),

    url(r'^nuevaActividadAjax/', nuevaActividadAjax, name='nuevaActividadAjax'),
    path('gestionObservacionObjetivos/<int:id>', GestionObservacionesObjetivos, name="gestionobservacionobjetivos"),
    path('gestionObservacionActividades/<int:id>', GestionObservacionesActividades, name="gestionobservacionactividades"),

    ]

