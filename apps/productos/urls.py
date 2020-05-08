from django.urls import path
from django.conf.urls import url
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [

    path('listar', login_required(views.ProductoList.as_view()), name='producto_listar'),
    path('create', login_required(views.ProductoCreate.as_view()), name='producto_crear'),
    path('edit/<int:pk>', login_required(views.ProductoEdit.as_view()), name='producto_editar'),
    path('delete/<int:pk>', login_required(views.ProductoDelete.as_view()), name='producto_delete'),
]