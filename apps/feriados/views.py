from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from apps.feriados.models import Ges_Feriados
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from apps.feriados.forms import feriadosForm
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from apps.periodos.models import Glo_Periodos
# Create your views here.
class feriadosList(ListView):
    model = Ges_Feriados
    template_name = 'feriados/feriados_list.html'

    def get_context_data(self, **kwargs):
        context = super(feriadosList, self).get_context_data(**kwargs)

        try:
            periodo_actual = Glo_Periodos.objects.get(id_estado=1)
        except Glo_Periodos.DoesNotExist:
            return None

        lista_horas = Ges_Feriados.objects.filter(id_periodo=periodo_actual.id)
        context['object_list'] = lista_horas
        return context


class FeriadoCreate(SuccessMessageMixin, CreateView):
    model = Ges_Feriados
    form_class = feriadosForm
    template_name = 'feriados/feriados_form.html'
   # success_url = reverse_lazy('feriados_list')


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
            return HttpResponseRedirect('/feriados/')
        else:
            request.session['message_class'] = "alert alert-danger"
            messages.error(self.request, "Error interno: No se ha creado el registro. Comuníquese con el administrador.")
            return HttpResponseRedirect('/feriados/')



class FeriadosUpdate(UpdateView):
    model = Ges_Feriados
    template_name = 'feriados/feriados_update.html'
    success_url = reverse_lazy('feriados_list')
    form_class = feriadosForm

    def feriados_update(request, pk, template_name='feriados/feriados_form.html'):
        feriados = get_object_or_404(Ges_Feriados, pk=pk)
        form = feriadosForm(request.POST or None, instance=feriados)
        if form.is_valid():
            form.save()
            return redirect('feriados_list')
        return render(request, template_name, {'form': form})

class FeriadosDelete(DeleteView):
    model = Ges_Feriados
    template_name = 'feriados/feriados_delete.html'
    success_url = reverse_lazy('feriados_list')


    def book_delete(request, pk, template_name='books/book_confirm_delete.html'):

        feriados = get_object_or_404(Ges_Feriados, pk=pk)
        if request.method == 'POST':
            feriados.delete()
            return redirect('feriados_list')
        return render(request, template_name, {'object': feriados})