from django.conf.urls import url
from apps.familia_cargo.views import familiadecargosList, FamiliaCargosCreate, FamiliaCargosUpdate,FamiliaCargosDelete
from django.contrib.auth.decorators import login_required

urlpatterns = [

    url('listarfcargo/', login_required(familiadecargosList.as_view()), name='familiadecargos_listar'),
    url(r'crear/', login_required(FamiliaCargosCreate.as_view()), name='FamiliaCargosCrear'),
    url('editar/(?P<pk>\d+)/$', login_required(FamiliaCargosUpdate.as_view()), name='FamiliaCargosEditar'),
    url('eliminar/(?P<pk>\d+)/$', login_required(FamiliaCargosDelete.as_view()), name='FamiliaCargosEliminar'),

]