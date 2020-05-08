from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from apps.estado_flujo.forms import estadoFlujoForm
from apps.estado_flujo.models import Glo_EstadoFlujo
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.db.models.deletion import ProtectedError
from datetime import date
# Create your views here.


class EstadoFlujoList(ListView):
    model = Glo_EstadoFlujo
    template_name = 'estado_flujo/estado_flujo_list.html'


class EstadoFlujoCreate(SuccessMessageMixin, CreateView):
    model = Glo_EstadoFlujo
    form_class = estadoFlujoForm
    template_name = 'estado_flujo/estado_flujo_form.html'


    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        if form.is_valid():
            form.save()
            request.session['message_class'] = "alert alert-success"
            messages.success(self.request, "Los datos fueron creados correctamente!")
            return HttpResponseRedirect('/estado_flujo/listar')
        else:
            request.session['message_class'] = "alert alert-danger"
            messages.error(self.request, "Error interno: No se ha creado el registro. Comuníquese con el administrador.")
            return HttpResponseRedirect('/estado_flujo/listar')



class EstadoFlujoEdit(SuccessMessageMixin, UpdateView ):
    model = Glo_EstadoFlujo
    form_class = estadoFlujoForm
    template_name = 'estado_flujo/estado_flujo_form.html'

    def post(self, request, *args, **kwargs):

        self.object = self.get_object
        id_periodicidad = kwargs['pk']
        instancia_nivel = self.model.objects.get(id=id_periodicidad)
        form = self.form_class(request.POST, instance=instancia_nivel)

        if form.is_valid():
            form.save()
            request.session['message_class'] = "alert alert-success"
            messages.success(self.request, "Los datos fueron actualizados correctamente!" )
            return HttpResponseRedirect('/estado_flujo/listar')
        else:
            request.session['message_class'] = "alert alert-danger"
            messages.error(self.request, "Error interno: No se ha actualizado el registro. Comuníquese con el administrador.")
            return HttpResponseRedirect('/estado_flujo/listar')


class EstadoFlujoDelete(SuccessMessageMixin, DeleteView ):
    model = Glo_EstadoFlujo
    template_name = 'estado_flujo/estado_flujo_delete.html'

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        try:
            obj.delete()
            request.session['message_class'] = "alert alert-success"
            messages.success(self.request, "El registro fue eliminado correctamente!")
            return HttpResponseRedirect('/estado_flujo/listar')

        except ProtectedError as e:
            request.session['message_class'] = "alert alert-danger"
            messages.error(request, "Error de integridad: Este nivel posee subniveles los que deben ser borrados antes de borrar este nivel.")
            return HttpResponseRedirect('/estado_flujo/listar')

        except Exception  as e:
            request.session['message_class'] = "alert alert-danger"
            messages.error(request, "Error interno: No se ha eliminado el registro. Comuníquese con el administrador.")
            return HttpResponseRedirect('/estado_flujo/listar')