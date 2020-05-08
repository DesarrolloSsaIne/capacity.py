from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect

from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models.deletion import ProtectedError
from apps.familia_cargo.models import Glo_FamiliaCargo
from apps.familia_cargo.forms import familiaCargoForm

class familiadecargosList(ListView):
    model = Glo_FamiliaCargo
    template_name = 'familiade_cargo/familia_list.html'

class FamiliaCargosCreate(CreateView):
    form_class = familiaCargoForm
    template_name = 'familiade_cargo/familia_form.html'

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        if form.is_valid():
            form.save()
            request.session['message_class'] = "alert alert-success"
            messages.success(self.request, "Los datos fueron creados correctamente!")
            return HttpResponseRedirect('/familiadecargos/listarfcargo')
        else:
            request.session['message_class'] = "alert alert-danger"
            messages.error(self.request, "Error interno: No se ha creado el registro. Comuníquese con el administrador.")
            return HttpResponseRedirect('/familiadecargos/listarfcargo')

class FamiliaCargosUpdate(SuccessMessageMixin, UpdateView ):
    model = Glo_FamiliaCargo
    form_class = familiaCargoForm
    template_name = 'familiade_cargo/familia_form.html'

    def post(self, request, *args, **kwargs):

        self.object = self.get_object
        id = kwargs['pk']
        glosa_familiaCargo = self.model.objects.get(id=id)
        form = self.form_class(request.POST, instance=glosa_familiaCargo)

        if form.is_valid():
            form.save()
            request.session['message_class'] = "alert alert-success"
            messages.success(self.request, "Los datos fueron actualizados correctamente!" )
            return HttpResponseRedirect('/familiadecargos/listarfcargo')
        else:
            request.session['message_class'] = "alert alert-danger"
            messages.error(self.request, "Error interno: No se ha actualizado el registro. Comuníquese con el administrador.")
            return HttpResponseRedirect('familiadecargos/listarfcargo')

class FamiliaCargosDelete(SuccessMessageMixin, DeleteView ):
    model = Glo_FamiliaCargo
    template_name = 'familiade_cargo/familia_delete.html'

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        try:
            obj.delete()
            request.session['message_class'] = "alert alert-success"
            messages.success(self.request, "El registro fue eliminado correctamente!")
            return HttpResponseRedirect('/familiadecargos/listarfcargo')

        except ProtectedError as e:
            request.session['message_class'] = "alert alert-warning"
            messages.error(request, "Alerta de integridad: Esta familia de cargo se encuentra asignada por lo cual no podrá ser borrada.")
            return HttpResponseRedirect('/familiadecargos/listarfcargo')


        except Exception  as e:
            request.session['message_class'] = "alert alert-danger"
            messages.error(request, "Error interno: No se ha eliminado el registro. Comuníquese con el administrador.")
            return HttpResponseRedirect('/familiadecargos/listarfcargo')