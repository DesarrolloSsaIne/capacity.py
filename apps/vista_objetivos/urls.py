from django.conf.urls import url, include
from apps.vista_objetivos.views import ObjetivosEstrategicosList
from django.contrib.auth.decorators import login_required

urlpatterns = [

    url(r'listar/', login_required(ObjetivosEstrategicosList.as_view()), name='ListarObjetivos'),



    ]