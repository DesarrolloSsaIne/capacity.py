from django.shortcuts import render
from django.contrib.auth.models import User, Group
from apps.controlador.models import Ges_Controlador
from apps.jefaturas.models import Ges_Jefatura
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models.deletion import ProtectedError
from django.db.models import Q
from django.db.models.deletion import ProtectedError

# Create your views here.


class PerfilesList(ListView):
    model = User
    template_name = 'perfiles/perfil_list.html'
    context_object_name = 'object_list'
    queryset = Group.objects.filter(~Q(id=6) &~Q(id=2) & ~Q(id=5) & ~Q(id=1))



class PerfilUsuarioList(ListView):
    model = Group
    template_name = 'perfiles/perfil_usuarios_list.html'

    def get_context_data(self, **kwargs):
        context = super(PerfilUsuarioList, self).get_context_data(**kwargs)

        qs = User.objects.filter(groups__in=Group.objects.filter(id=self.kwargs['pk']))
        grupo = Group.objects.get(id=self.kwargs['pk'])

        context['object_list'] = qs
        context['grupo']= grupo
        self.request.session["id_perfil"] = self.kwargs['pk']

        return context


def PerfilDelete(request, id):
    template_name = 'perfiles/perfil_delete.html'


    if request.method == "POST": # aquí recojo lo que trae el modal


        try:
            id_perfil = request.session["id_perfil"]

            g = Group.objects.get(user=id)
            g.user_set.remove(id)

            request.session['message_class'] = "alert alert-success" #Tipo mensaje
            messages.success(request, "Los usuario fue eliminado correctamente de este perfil!") # mensaje
            return HttpResponseRedirect('/perfiles/listarUsuarios/' + str(id_perfil)) # Redirije a la pantalla principal

        except ProtectedError:
            request.session['message_class'] = "alert alert-danger" #Tipo mensaje
            messages.success(request, "No puede eliminar este dato ya que se encuentra asociado a otro registro!") # mensaje
            return HttpResponseRedirect('/perfiles/listarUsuarios/' + str(id_perfil)) # Redirije a la pantalla principal


    return render(request, template_name)



def PerfilAsigna(request):
    template_name = 'perfiles/perfil_form.html'

    jefes_list = list(Ges_Jefatura.objects.values_list('id_user_id', flat=True))
    qs = User.objects.filter(id__in=jefes_list).exclude(Q(groups__in=Group.objects.all())) #Usuarios que están en la lista de jefaturas pero no han sido asignados a un perfil

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


######################################################################################################################

class PerfilesListAnalistas(ListView):
    model = Group
    template_name = 'perfiles/perfil_analistas_list.html'

    def get_context_data(self, **kwargs):
        context = super(PerfilesListAnalistas, self).get_context_data(**kwargs)

        qs = User.objects.filter(groups__in=Group.objects.filter(id=6))
        grupo = Group.objects.get(id=6)

        context['object_list'] = qs
        context['grupo']= grupo
        self.request.session["id_perfil"] = 6

        return context



def PerfilDeleteAnalista(request, id):
    template_name = 'perfiles/perfil_delete.html'


    if request.method == "POST": # aquí recojo lo que trae el modal


        try:
            id_perfil = request.session["id_perfil"]

            g = Group.objects.get(user=id)
            g.user_set.remove(id)

            request.session['message_class'] = "alert alert-success" #Tipo mensaje
            messages.success(request, "Los usuario fue eliminado correctamente de este perfil!") # mensaje
            return HttpResponseRedirect('/perfiles/listarAnalistas/') # Redirije a la pantalla principal

        except ProtectedError:
            request.session['message_class'] = "alert alert-danger" #Tipo mensaje
            messages.success(request, "No puede eliminar este dato ya que se encuentra asociado a otro registro!") # mensaje
            return HttpResponseRedirect('/perfiles/listarAnalistas/') # Redirije a la pantalla principal


    return render(request, template_name)



def PerfilAsignaAnalista(request):
    template_name = 'perfiles/perfil_form.html'

    jefes_list = list(Ges_Jefatura.objects.values_list('id_user_id', flat=True))

    # self.fields['id_user'].queryset = User.objects.all().exclude(id__in=jefes_list)

    qs = User.objects.exclude(Q(groups__in=Group.objects.all()) | Q(id__in=jefes_list)) #Envío los usuario que no pertenezcan a algún grupo.

    context = {"qs": qs} # aquí le envío lo que quiero al modal para que lo muestre, incluso una lista.

    if request.method == "POST": # aquí recojo lo que trae el modal
        id_perfil = request.session["id_perfil"]
        id_user= request.POST['SelectUser'] # aquí capturo lo que traigo del modal

        g = Group.objects.get(id=id_perfil)
        g.user_set.add(id_user)


        request.session['message_class'] = "alert alert-success" #Tipo mensaje
        messages.success(request, "El perfil fue agregado correctamente!") # mensaje
        return HttpResponseRedirect('/perfiles/listarAnalistas/') # Redirije a la pantalla principal
#
    return render(request, template_name, context)