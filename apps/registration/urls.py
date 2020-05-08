from django.urls import path
from apps.registration.views import login, logout
from django.conf.urls import url, include
from apps.registration.views import LogList
app_name = 'registration'
urlpatterns = [


    path('login/', login, name="login"),
    path('logout/', logout, name="logout"),
    url(r'listar/', LogList.as_view(), name='LogListar'),



]