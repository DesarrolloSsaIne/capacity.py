from django.urls import path
from django.conf.urls import url
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [

    path('', login_required(views.feriadosList.as_view()), name='feriados_list'),
    path('new', login_required(views.FeriadoCreate.as_view()), name='feriado_new'),
    path('edit/<int:pk>', login_required(views.FeriadosUpdate.as_view()), name='feriado_edit'),
    path('delete/<int:pk>', login_required(views.FeriadosDelete.as_view()), name='feriado_delete'),
]