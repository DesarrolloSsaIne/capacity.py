from django.conf.urls import url, include
from apps.planificacion_admin.views import PlanificacionAdminList, AsignaAnalista
from django.contrib.auth.decorators import login_required
from django.urls import path

urlpatterns = [


    # url(r'crear/', login_required(JefaturaCreate.as_view()), name='JefaturaCrear'),
    url(r'listar/', login_required(PlanificacionAdminList.as_view()), name='PlanificacionAdminListar'),
    path('asigna/<int:id>', login_required(AsignaAnalista), name='PlanificacionAdminAsigna'),
    # url('eliminar/(?P<pk>\d+)/$', login_required(JefaturaDelete.as_view()), name='JefaturaEliminar'),


    #url('editar/2/(?P<id_nivel>\d+)/$', SegundoNivelUpdate, name='SegundoNivelEditar'),

]