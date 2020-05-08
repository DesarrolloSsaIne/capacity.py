from django.shortcuts import render
from apps.eje.models import Ges_Ejes
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from apps.eje.forms import EjeForm
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.db.models.deletion import ProtectedError
from apps.periodos.models import Glo_Periodos
# Create your views here.
class EjeList(ListView):
    model = Ges_Ejes
    template_name = 'eje/eje_list.html'

    def get_context_data(self, **kwargs):
        context = super(EjeList, self).get_context_data(**kwargs)

        try:
            periodo_actual = Glo_Periodos.objects.get(id_estado=1)
        except Glo_Periodos.DoesNotExist:
            return None

        lista_horas = Ges_Ejes.objects.filter(id_periodo=periodo_actual.id)
        context['object_list'] = lista_horas
        return context


class EjeCreate(SuccessMessageMixin, CreateView):
        form_class = EjeForm
        template_name = 'eje/eje_form.html'

        def post(self, request, *args, **kwargs):
            form_class = self.get_form_class()
            form = self.get_form(form_class)
            try:
                periodo_activo = Glo_Periodos.objects.get(id_estado=1)
            except Glo_Periodos.DoesNotExist:
                return None


            if form.is_valid():
                form.instance.id_periodo = periodo_activo
                form.save()
                request.session['message_class'] = "alert alert-success"
                messages.success(self.request, "Los datos fueron creados correctamente!")
                return HttpResponseRedirect('/ejes/listar')
            else:
                request.session['message_class'] = "alert alert-danger"
                messages.error(self.request,
                               "Error interno: No se ha creado el registro. Comuníquese con el administrador.")
                return HttpResponseRedirect(request, '/ejes/listar')

class EjeUpdate(UpdateView):
    model = Ges_Ejes
    form_class = EjeForm
    template_name = 'eje/eje_form.html'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        id_nivel = kwargs['pk']
        instancia_nivel = self.model.objects.get(id=id_nivel)
        form = self.form_class(request.POST, instance=instancia_nivel)

        if form.is_valid():
            form.save()
            request.session['message_class'] = "alert alert-success"
            messages.success(self.request, "Los datos fueron actualizados correctamente!")
            return HttpResponseRedirect('/ejes/listar')
        else:
            request.session['message_class'] = "alert alert-danger"
            messages.error(self.request, "Error interno: No se ha eliminado el registro. Comuníquese con el administrador.")
            return HttpResponseRedirect('/ejes/listar')

class EjeDelete(SuccessMessageMixin, DeleteView ):
    model = Ges_Ejes
    template_name = 'eje/eje_delete.html'

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        try:
            obj.delete()
            request.session['message_class'] = "alert alert-success"
            messages.success(self.request, "El registro fue eliminado correctamente!")
            return HttpResponseRedirect('/ejes/listar/')

        except ProtectedError as e:
            request.session['message_class'] = "alert alert-danger"
            messages.error(request, "Error de integridad: Este nivel posee subniveles los que deben ser borrados antes de borrar este nivel.")
            return HttpResponseRedirect('/ejes/listar')

        except Exception  as e:
            request.session['message_class'] = "alert alert-danger"
            messages.error(request, "Error interno: No se ha eliminado el registro. Comuníquese con el administrador.")
            return HttpResponseRedirect('/ejes/listar')