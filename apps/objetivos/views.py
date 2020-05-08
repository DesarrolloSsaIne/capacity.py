from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
# Create your views here.
from apps.objetivos.models import Ges_Objetivo_Estrategico, Ges_Objetivo_Tactico, Ges_Objetivo_Operativo,Ges_Objetivo_TacticoTN
from apps.estructura.models import Ges_PrimerNivel
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.list import MultipleObjectMixin
from apps.objetivos.forms import ObjetivosEstrategicosForm, ObjetivosTacticosForm_sn, ObjetivosTacticosForm_sn_new, ObjetivosOperativosForm, ObjetivosTacticosForm_tn_new,ObjetivosTacticosFormEdit_tn_new
from django.db.models.deletion import ProtectedError
from apps.estructura.models import Ges_SegundoNivel, Ges_TercerNivel, Ges_CuartoNivel
from django.shortcuts import get_object_or_404
from django.core.serializers.json import Serializer
from apps.periodos.models import Glo_Periodos
from django.urls import reverse_lazy
from django.db.models import Q
############GESTIÓN OBJETIVOS ESTRATEGICOS##########################

class ObjetivosEstrategicosList(ListView):
    model = Ges_Objetivo_Estrategico
    template_name = 'objetivos/objetivos_estrategicos_list.html'

    def get_context_data(self, **kwargs):
        context = super(ObjetivosEstrategicosList, self).get_context_data(**kwargs)

        try:
            periodo_actual = Glo_Periodos.objects.get(id_estado=1)
        except Glo_Periodos.DoesNotExist:
            return None

        lista_horas = Ges_Objetivo_Estrategico.objects.filter(id_periodo=periodo_actual.id)
        context['object_list'] = lista_horas
        return context

class ObjetivosEstrategicosCreate(SuccessMessageMixin, CreateView ):
    form_class = ObjetivosEstrategicosForm
    template_name = 'objetivos/objetivos_estrategicos_form.html'


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
            return HttpResponseRedirect('/objetivos/estrategicos/listar/')
        else:
            request.session['message_class'] = "alert alert-danger"
            messages.error(self.request, "Error interno: No se ha creado el registro. Comuníquese con el administrador.")
            return HttpResponseRedirect('/objetivos/estrategicos/listar/')


class ObjetivosEstrategicosEdit(SuccessMessageMixin, UpdateView ):
    model = Ges_Objetivo_Estrategico
    form_class = ObjetivosEstrategicosForm
    template_name = 'objetivos/objetivos_estrategicos_form.html'

    def post(self, request, *args, **kwargs):

        self.object = self.get_object
        id_nivel = kwargs['pk']
        instancia_nivel = self.model.objects.get(id=id_nivel)
        form = self.form_class(request.POST, instance=instancia_nivel)

        if form.is_valid():
            form.save()
            request.session['message_class'] = "alert alert-success"
            messages.success(self.request, "Los datos fueron actualizados correctamente!" )
            return HttpResponseRedirect('/objetivos/estrategicos/listar/')
        else:
            request.session['message_class'] = "alert alert-danger"
            messages.error(self.request, "Error interno: No se ha actualizado el registro. Comuníquese con el administrador.")
            return HttpResponseRedirect('/objetivos/estrategicos/listar/')


class ObjetivosEstrategicosDelete(SuccessMessageMixin, DeleteView ):
    model = Ges_Objetivo_Estrategico
    template_name = 'objetivos/objetivos_delete.html'

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        try:
            obj.delete()
            request.session['message_class'] = "alert alert-success"
            messages.success(self.request, "El registro fue eliminado correctamente!")
            return HttpResponseRedirect('/objetivos/estrategicos/listar/')

        except ProtectedError as e:
            request.session['message_class'] = "alert alert-danger"
            messages.error(request, "Error de integridad: Este nivel posee subniveles los que deben ser borrados antes de borrar este nivel.")
            return HttpResponseRedirect('/objetivos/estrategicos/listar/')

        except Exception  as e:
            request.session['message_class'] = "alert alert-danger"
            messages.error(request, "Error interno: No se ha eliminado el registro. Comuníquese con el administrador.")
            return HttpResponseRedirect('/objetivos/estrategicos/listar/')

############FIN GESTIÓN OBJETIVOS ESTRATEGICOS##########################

############GESTIÓN OBJETIVOS TACTICOS PARA SEGUNDO NIVEL ##########################


class ObjetivosTacticosDetail(ListView):
    model = Ges_Objetivo_Tactico
    template_name = 'objetivos/objetivos_tacticos_detail.html'



    def get_context_data(self,  **kwargs):
        context = super(ObjetivosTacticosDetail, self).get_context_data(**kwargs)

        try:
            periodo_actual = Glo_Periodos.objects.get(id_estado=1)
        except Glo_Periodos.DoesNotExist:
            return None

        lista_objetivos = Ges_Objetivo_Tactico.objects.filter(Q(id_segundo_nivel=self.kwargs['pk']) & Q(id_periodo=periodo_actual.id))
        context['object_list'] = lista_objetivos
        self.request.session['id_tercer_nivel']=self.kwargs['pk']
        return context


class ObjetivosTacticosEdit(SuccessMessageMixin, UpdateView ):
    model = Ges_Objetivo_Tactico
    form_class = ObjetivosTacticosForm_sn
    template_name = 'objetivos/objetivos_tacticos_form_new.html'

    def post(self, request, *args, **kwargs):

        self.object = self.get_object
        id_nivel = kwargs['pk']
        id_nivel_superior = Ges_Objetivo_Tactico.objects.get(id=id_nivel)
        instancia_nivel = self.model.objects.get(id=id_nivel)
        form = self.form_class(request.POST, instance=instancia_nivel)

        if form.is_valid():
            form.save()
            request.session['message_class'] = "alert alert-success"
            messages.success(self.request, "Los datos fueron actualizados correctamente!" )

            return HttpResponseRedirect('/objetivos/tacticos/sn/detail/'+ str(id_nivel_superior.id_segundo_nivel_id))
        else:
            request.session['message_class'] = "alert alert-danger"
            messages.error(self.request, "Error interno: No se ha actualizado el registro. Comuníquese con el administrador.")
            return HttpResponseRedirect('/objetivos/tacticos/sn/detail/' + str(id_nivel_superior.id_segundo_nivel_id))



class ObjetivosTacticosDelete(SuccessMessageMixin, DeleteView ):
    model = Ges_Objetivo_Tactico
    template_name = 'objetivos/objetivos_delete.html'


    def delete(self, request, *args, **kwargs):


        obj = self.get_object()
        lista_objetivo = Ges_Objetivo_Tactico.objects.get(id=self.kwargs['pk'])
        id_nivel_superior = lista_objetivo.id_segundo_nivel_id

        try:
            obj.delete()

            request.session['message_class'] = "alert alert-success"
            messages.success(self.request, "El registro fue eliminado correctamente!")
            return HttpResponseRedirect('/objetivos/tacticos/sn/detail/' + str(id_nivel_superior))

        except ProtectedError as e:
            request.session['message_class'] = "alert alert-danger"
            messages.error(request, "Error de integridad: Este nivel posee subniveles los que deben ser borrados antes de borrar este nivel.")
            return HttpResponseRedirect('/objetivos/tacticos/sn/detail/'  + str(id_nivel_superior))

        except Exception  as e:
            request.session['message_class'] = "alert alert-danger"
            messages.error(request, "Error interno: No se ha eliminado el registro. Comuníquese con el administrador.")


class ObjetivosTacticosCreate(SuccessMessageMixin, CreateView ):
    model = Ges_Objetivo_Tactico
    form_class = ObjetivosTacticosForm_sn_new
    template_name = 'objetivos/objetivos_tacticos_form_new.html'


    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        id_nivel_superior = self.request.session['id_tercer_nivel']
        # obtiene el id_nivel_superior desde la url para no perderla al momento de hacer el post de guardado

        try:
            periodo_activo = Glo_Periodos.objects.get(id_estado=1)
        except Glo_Periodos.DoesNotExist:
            return None


        if form.is_valid():

            form.instance.id_segundo_nivel_id = str(id_nivel_superior)

            # agrega el campo ges_segundo_nivel_id, para no traerlo desde el template.

            form.instance.id_periodo = periodo_activo
            form.save()

            request.session['message_class'] = "alert alert-success"
            messages.success(self.request, "Los datos fueron creados correctamente!")
            return HttpResponseRedirect('/objetivos/tacticos/sn/detail/'+ str(id_nivel_superior))
        else:
            request.session['message_class'] = "alert alert-danger"
            messages.error(self.request, "Error interno: No se ha creado el registro. Comuníquese con el administrador.")
            return HttpResponseRedirect('/objetivos/tacticos/sn/detail/'+ str(id_nivel_superior))


############ FIN GESTIÓN OBJETIVOS TACTICOS PARA SEGUNDO NIVEL ##########################



############GESTIÓN OBJETIVOS TACTICOS PARA TERCER NIVEL ##########################

class ObjetivosTacticosDetailTN(ListView):
    model = Ges_Objetivo_TacticoTN
    template_name = 'objetivos/objetivos_tacticos_detailTN.html'




    def get_context_data(self,  **kwargs):
        context = super(ObjetivosTacticosDetailTN, self).get_context_data(**kwargs)
        try:
            periodo_actual = Glo_Periodos.objects.get(id_estado=1)
        except Glo_Periodos.DoesNotExist:
            return None

        lista_objetivos = Ges_Objetivo_TacticoTN.objects.filter(Q(id_tercer_nivel=self.kwargs['pk']) & Q(id_periodo=periodo_actual.id))
        context['object_list'] = lista_objetivos
        self.request.session['id_tercer_nivel']=self.kwargs['pk']
        return context

class ObjetivosTacticosCreateTN(SuccessMessageMixin, CreateView ):
    model = Ges_Objetivo_TacticoTN
    form_class = ObjetivosTacticosForm_tn_new
    template_name = 'objetivos/objetivos_taticos_form_newTN.html'



    def get_form_kwargs(self, **kwargs):
        kwargs = super(ObjetivosTacticosCreateTN, self).get_form_kwargs()
        segundo_nivel=Ges_TercerNivel.objects.get(id=self.request.session['id_tercer_nivel'])
        kwargs['id_segundo_nivel'] = segundo_nivel.segundo_nivel_id
        return kwargs



    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        id_nivel_superior = self.request.session['id_tercer_nivel']
        # obtiene el id_nivel_superior desde la url para no perderla al momento de hacer el post de guardado

        try:
            periodo_activo = Glo_Periodos.objects.get(id_estado=1)
        except Glo_Periodos.DoesNotExist:
            return None

        if form.is_valid():

            form.instance.id_tercer_nivel_id = str(id_nivel_superior)

            # agrega el campo ges_segundo_nivel_id, para no traerlo desde el template.
            form.instance.id_periodo = periodo_activo
            form.save()

            request.session['message_class'] = "alert alert-success"
            messages.success(self.request, "Los datos fueron creados correctamente!")
            return HttpResponseRedirect('/objetivos/tacticos/tn/detail/'+ str(id_nivel_superior))

        else:
            request.session['message_class'] = "alert alert-danger"
            messages.error(self.request, "Error interno: No se ha creado el registro. Comuníquese con el administrador.")
            return HttpResponseRedirect('/objetivos/tacticos/tn/detail/'+ str(id_nivel_superior))


class ObjetivosTacticosEditTN(SuccessMessageMixin, UpdateView):
    model = Ges_Objetivo_TacticoTN
    form_class = ObjetivosTacticosFormEdit_tn_new
    template_name = 'objetivos/objetivos_taticos_form_newTN.html'
    success_message = ("Los datos fueron actualizados correctamente!" )


    def get_form_kwargs(self, **kwargs):
        kwargs = super(ObjetivosTacticosEditTN, self).get_form_kwargs()
        segundo_nivel=Ges_TercerNivel.objects.get(id=self.request.session['id_tercer_nivel'])
        kwargs['id_segundo_nivel'] = segundo_nivel.segundo_nivel_id

        return kwargs

    def get_success_url(self):
        lista_objetivo = Ges_Objetivo_TacticoTN.objects.get(id=self.kwargs['pk'])
        id_nivel_superior = lista_objetivo.id_tercer_nivel_id
        return reverse_lazy('ObjetivosTacticosDetalleTN', args=(id_nivel_superior,))






class ObjetivosTacticosDeleteTN(SuccessMessageMixin, DeleteView ):
    model = Ges_Objetivo_TacticoTN
    template_name = 'objetivos/objetivos_delete.html'


    def delete(self, request, *args, **kwargs):


        obj = self.get_object()
        lista_objetivo = Ges_Objetivo_TacticoTN.objects.get(id=self.kwargs['pk'])
        id_nivel_superior = lista_objetivo.id_tercer_nivel_id

        try:
            obj.delete()

            request.session['message_class'] = "alert alert-success"
            messages.success(self.request, "El registro fue eliminado correctamente!")
            return HttpResponseRedirect('/objetivos/tacticos/tn/detail/' + str(id_nivel_superior))

        except ProtectedError as e:
            request.session['message_class'] = "alert alert-warning"
            messages.error(request, "Alerta de integridad: Este nivel posee subniveles los que deben ser borrados antes de borrar este nivel.")
            return HttpResponseRedirect('/objetivos/tacticos/tn/detail/'  + str(id_nivel_superior))

        except Exception  as e:
            request.session['message_class'] = "alert alert-danger"
            messages.error(request, "Error interno: No se ha eliminado el registro. Comuníquese con el administrador.")


############FIN GESTIÓN OBJETIVOS TACTICOS PARA TERCER NIVEL ##########################


############GESTIÓN OBJETIVOS OPERATIVOS ##########################

class ObjetivosOperativosDetail(ListView):
    model = Ges_Objetivo_Operativo
    template_name = 'objetivos/objetivos_operativos_detail.html'


    def get_context_data(self,  **kwargs):
        context = super(ObjetivosOperativosDetail, self).get_context_data(**kwargs)

        try:
            periodo_actual = Glo_Periodos.objects.get(id_estado=1)
        except Glo_Periodos.DoesNotExist:
            return None
        lista_objetivos = Ges_Objetivo_Operativo.objects.filter(Q(id_cuarto_nivel=self.kwargs['pk']) & Q(id_periodo=periodo_actual.id))
        context['object_list'] = lista_objetivos
        self.request.session['id_cuarto_nivel']=self.kwargs['pk']
        return context

class ObjetivosOperativosCreate(SuccessMessageMixin, CreateView ):
    model = Ges_Objetivo_Operativo
    form_class = ObjetivosOperativosForm
    template_name = 'objetivos/objetivos_operativos_form.html'

    def get_form_kwargs(self, **kwargs):
        kwargs = super(ObjetivosOperativosCreate, self).get_form_kwargs()
        tercer_nivel=Ges_CuartoNivel.objects.get(id=self.request.session['id_cuarto_nivel'])
        kwargs['id_tercer_nivel'] = tercer_nivel.tercer_nivel_id
        return kwargs


    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        id_nivel_superior = self.request.session['id_cuarto_nivel']
        # obtiene el id_nivel_superior desde la url para no perderla al momento de hacer el post de guardado

        try:
            periodo_activo = Glo_Periodos.objects.get(id_estado=1)
        except Glo_Periodos.DoesNotExist:
            return None

        if form.is_valid():

            form.instance.id_cuarto_nivel_id = str(id_nivel_superior)
            # agrega el campo ges_segundo_nivel_id, para no traerlo desde el template.
            form.instance.id_periodo = periodo_activo
            form.save()

            request.session['message_class'] = "alert alert-success"
            messages.success(self.request, "Los datos fueron creados correctamente!")
            return HttpResponseRedirect('/objetivos/operativos/detail/'+ str(id_nivel_superior))

        else:
            request.session['message_class'] = "alert alert-danger"
            messages.error(self.request, "Error interno: No se ha creado el registro. Comuníquese con el administrador.")
            return HttpResponseRedirect('/objetivos/operativos/detail/'+ str(id_nivel_superior))


class ObjetivosOperativosEdit(SuccessMessageMixin, UpdateView ):
    model = Ges_Objetivo_Operativo
    form_class = ObjetivosOperativosForm
    template_name = 'objetivos/objetivos_operativos_form.html'
    success_message = ("Los datos fueron actualizados correctamente!" )

    def get_form_kwargs(self, **kwargs):
        kwargs = super(ObjetivosOperativosEdit, self).get_form_kwargs()
        tercer_nivel=Ges_CuartoNivel.objects.get(id=self.request.session['id_cuarto_nivel'])
        kwargs['id_tercer_nivel'] = tercer_nivel.tercer_nivel_id
        return kwargs


    def get_success_url(self):
        id_nivel = self.kwargs['pk']
        id_nivel_superior = Ges_Objetivo_Operativo.objects.get(id=id_nivel)
        return reverse_lazy('ObjetivosOperativosDetail', args=(id_nivel_superior.id_cuarto_nivel_id,))



class ObjetivosOperativosDelete(SuccessMessageMixin, DeleteView ):
    model = Ges_Objetivo_Operativo
    template_name = 'objetivos/objetivos_delete.html'


    def delete(self, request, *args, **kwargs):


        obj = self.get_object()
        lista_objetivo = Ges_Objetivo_Operativo.objects.get(id=self.kwargs['pk'])
        id_nivel_superior = lista_objetivo.id_cuarto_nivel_id

        try:
            obj.delete()

            request.session['message_class'] = "alert alert-success"
            messages.success(self.request, "El registro fue eliminado correctamente!")
            return HttpResponseRedirect('/objetivos/operativos/detail/' + str(id_nivel_superior))

        except ProtectedError as e:
            request.session['message_class'] = "alert alert-danger"
            messages.error(request, "Error de integridad: Este nivel posee subniveles los que deben ser borrados antes de borrar este nivel.")
            return HttpResponseRedirect('/objetivos/operativos/detail/'  + str(id_nivel_superior))

        except Exception  as e:
            request.session['message_class'] = "alert alert-danger"
            messages.error(request, "Error interno: No se ha eliminado el registro. Comuníquese con el administrador.")

############FIN GESTIÓN OBJETIVOS  OPERATIVOS  ##########################