from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from apps.periodicidad.forms import periodicidadForm
from apps.periodicidad.models import Glo_Periodicidad
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.db.models.deletion import ProtectedError
from datetime import date
# Create your views here.


class PeriodicidadList(ListView):
    model = Glo_Periodicidad
    template_name = 'periodicidad/periodicidad_list.html'


class PeriodicidadCreate(SuccessMessageMixin, CreateView):
    model = Glo_Periodicidad
    form_class = periodicidadForm
    template_name = 'periodicidad/periodicidad_form.html'


    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        if form.is_valid():
            form.instance.fecha_inicio= date.today()
            form.save()
            request.session['message_class'] = "alert alert-success"
            messages.success(self.request, "Los datos fueron creados correctamente!")
            return HttpResponseRedirect('/periodicidad/listar')
        else:
            request.session['message_class'] = "alert alert-danger"
            messages.error(self.request, "Error interno: No se ha creado el registro. Comuníquese con el administrador.")
            return HttpResponseRedirect('/periodicidad/listar')



class PeriodicidadEdit(SuccessMessageMixin, UpdateView ):
    model = Glo_Periodicidad
    form_class = periodicidadForm
    template_name = 'periodicidad/periodicidad_form.html'

    def post(self, request, *args, **kwargs):

        self.object = self.get_object
        id_periodicidad = kwargs['pk']
        instancia_nivel = self.model.objects.get(id=id_periodicidad)
        form = self.form_class(request.POST, instance=instancia_nivel)

        if form.is_valid():
            form.save()
            request.session['message_class'] = "alert alert-success"
            messages.success(self.request, "Los datos fueron actualizados correctamente!" )
            return HttpResponseRedirect('/periodicidad/listar')
        else:
            request.session['message_class'] = "alert alert-danger"
            messages.error(self.request, "Error interno: No se ha actualizado el registro. Comuníquese con el administrador.")
            return HttpResponseRedirect('/periodicidad/listar')


class PeriodicidadDelete(SuccessMessageMixin, DeleteView ):
    model = Glo_Periodicidad
    template_name = 'periodicidad/periodicidad_delete.html'

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        try:
            obj.delete()
            request.session['message_class'] = "alert alert-success"
            messages.success(self.request, "El registro fue eliminado correctamente!")
            return HttpResponseRedirect('/periodicidad/listar')

        except ProtectedError as e:
            request.session['message_class'] = "alert alert-danger"
            messages.error(request, "Error de integridad: Este nivel posee subniveles los que deben ser borrados antes de borrar este nivel.")
            return HttpResponseRedirect('/periodicidad/listar')

        except Exception  as e:
            request.session['message_class'] = "alert alert-danger"
            messages.error(request, "Error interno: No se ha eliminado el registro. Comuníquese con el administrador.")
            return HttpResponseRedirect('/periodicidad/listar')
