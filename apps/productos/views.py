from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from apps.productos.forms import productoForm
from apps.productos.models import Glo_ProductosEstadisticos
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.db.models.deletion import ProtectedError
from datetime import date
from apps.periodos.models import Glo_Periodos
# Create your views here.


class ProductoList(ListView):
    model = Glo_ProductosEstadisticos
    template_name = 'productos/productos_list.html'

    def get_context_data(self, **kwargs):
        context = super(ProductoList, self).get_context_data(**kwargs)

        try:
            periodo_actual = Glo_Periodos.objects.get(id_estado=1)
        except Glo_Periodos.DoesNotExist:
            return None

        lista_horas = Glo_ProductosEstadisticos.objects.filter(id_periodo=periodo_actual.id)
        context['object_list'] = lista_horas
        return context

class ProductoCreate(SuccessMessageMixin, CreateView):
    model = Glo_ProductosEstadisticos
    form_class = productoForm
    template_name = 'productos/productos_form.html'


    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        try:
            periodo_activo = Glo_Periodos.objects.get(id_estado=1)
        except Glo_Periodos.DoesNotExist:
            return None


        if form.is_valid():
            form.instance.fecha_inicio= date.today()

            form.instance.id_periodo = periodo_activo
            form.save()
            request.session['message_class'] = "alert alert-success"
            messages.success(self.request, "Los datos fueron creados correctamente!")
            return HttpResponseRedirect('/productos/listar')
        else:
            request.session['message_class'] = "alert alert-danger"
            messages.error(self.request, "Error interno: No se ha creado el registro. Comuníquese con el administrador.")
            return HttpResponseRedirect('/productos/listar')



class ProductoEdit(SuccessMessageMixin, UpdateView ):
    model = Glo_ProductosEstadisticos
    form_class = productoForm
    template_name = 'productos/productos_form.html'

    def post(self, request, *args, **kwargs):

        self.object = self.get_object
        id_periodicidad = kwargs['pk']
        instancia_nivel = self.model.objects.get(id=id_periodicidad)
        form = self.form_class(request.POST, instance=instancia_nivel)

        if form.is_valid():
            form.save()
            request.session['message_class'] = "alert alert-success"
            messages.success(self.request, "Los datos fueron actualizados correctamente!" )
            return HttpResponseRedirect('/productos/listar')
        else:
            request.session['message_class'] = "alert alert-danger"
            messages.error(self.request, "Error interno: No se ha actualizado el registro. Comuníquese con el administrador.")
            return HttpResponseRedirect('/productos/listar')


class ProductoDelete(SuccessMessageMixin, DeleteView ):
    model = Glo_ProductosEstadisticos
    template_name = 'productos/productos_delete.html'

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        try:
            obj.delete()
            request.session['message_class'] = "alert alert-success"
            messages.success(self.request, "El registro fue eliminado correctamente!")
            return HttpResponseRedirect('/productos/listar')

        except ProtectedError as e:
            request.session['message_class'] = "alert alert-danger"
            messages.error(request, "Error de integridad: Este nivel posee subniveles los que deben ser borrados antes de borrar este nivel.")
            return HttpResponseRedirect('/productos/listar')

        except Exception  as e:
            request.session['message_class'] = "alert alert-danger"
            messages.error(request, "Error interno: No se ha eliminado el registro. Comuníquese con el administrador.")
            return HttpResponseRedirect('/productos/listar')
