from django.shortcuts import render
from django.contrib.auth.models import User, Group
from apps.controlador.models import Ges_Controlador
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models.deletion import ProtectedError
from django.db.models import Q

# Create your views here.


class PerfilesList(ListView):
    model = User
    template_name = 'perfiles/perfil_list.html'

    def get_context_data(self, **kwargs):
        context = super(PerfilesList, self).get_context_data(**kwargs)

        lista_grupos =Group.objects.filter(~Q(id=2) & ~Q(id=5))
        context['object_list'] = lista_grupos
        return context



def PerfilUsuarioList(request, id):
    template_name = 'perfiles/perfil_usuarios_list.html'

    qs = User.objects.filter(groups__in=Group.objects.filter(id=id)) #Envío los usuario que no pertenezcan a algún grupo.
    grupo = Group.objects.get(id=id)


    context = {"object_list": qs, "grupo": grupo}

    request.session["id_perfil"]=id

    return render(request, template_name, context)



def PerfilDelete(request, id):
    template_name = 'perfiles/perfil_delete.html'


    if request.method == "POST": # aquí recojo lo que trae el modal

        g = Group.objects.get(user=id)
        g.user_set.remove(id)

        id_perfil= request.session["id_perfil"]
        request.session['message_class'] = "alert alert-success" #Tipo mensaje
        messages.success(request, "Los usuario fue eliminado correctamente de este perfil!") # mensaje
        return HttpResponseRedirect('/perfiles/listarUsuarios/' + str(id_perfil)) # Redirije a la pantalla principal

    return render(request, template_name)



def PerfilAsigna(request):
    template_name = 'perfiles/perfil_form.html'

    qs = User.objects.exclude(groups__in=Group.objects.all()) #Envío los usuario que no pertenezcan a algún grupo.
    context = {"qs": qs} # aquí le envío lo que quiero al modal para que lo muestre, incluso una lista.

    if request.method == "POST": # aquí recojo lo que trae el modal
        id_perfil = request.session["id_perfil"]
        id_user= request.POST['SelectUser'] # aquí capturo lo que traigo del modal

        g = Group.objects.get(id=id_perfil)
        g.user_set.add(id_user)


        request.session['message_class'] = "alert alert-success" #Tipo mensaje
        messages.success(request, "El perfil fue agregado correctamente!") # mensaje
        return HttpResponseRedirect('/perfiles/listarUsuarios/' + str(id_perfil)) # Redirije a la pantalla principal
#
    return render(request, template_name, context)