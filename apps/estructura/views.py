from django.shortcuts import render
from apps.estructura.models import Ges_PrimerNivel, Ges_SegundoNivel, Ges_TercerNivel, Ges_CuartoNivel, Ges_Niveles
from apps.estructura.forms import PrimerNivelForm, SegundoNivelForm, TercerNivelForm, CuartoNivelForm
from apps.objetivos.models import Ges_Objetivo_Estrategico, Ges_Objetivo_Tactico

from django.contrib.auth.models import User
# Create your views here.
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.views import generic
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string
from . import mixins
import json
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models.deletion import ProtectedError
from django.db.models import Q
from itertools import chain
from django.db.models import Sum
from django.db.models import Count
from apps.periodos.models import Glo_Periodos

############GESTIÓN PRIMER NIVEL##########################
def UpdatePrimerNivel(id_primer_nivel, descripcion_nivel):
    IdPrimero = Ges_Niveles.objects.get(id_primer_nivel=id_primer_nivel)
    Ges_Niveles.objects.filter(id=IdPrimero.id).update(
        descripcion_nivel=descripcion_nivel,

    )
    return None



class PrimerNivelList(ListView):
    model = Ges_PrimerNivel
    template_name = 'estructura/estructura_list_pn.html'

    def get_context_data(self, **kwargs):
        context = super(PrimerNivelList, self).get_context_data(**kwargs)

        try:
            periodo_actual = Glo_Periodos.objects.get(id_estado=1)
        except Glo_Periodos.DoesNotExist:
            return None

        lista_horas = Ges_PrimerNivel.objects.filter(id_periodo=periodo_actual.id)
        context['object_list'] = lista_horas
        return context


class PrimerNivelUpdate(UpdateView):
    model = Ges_PrimerNivel
    form_class = PrimerNivelForm
    template_name = 'estructura/estructura_form_pn.html'


    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        id_nivel = kwargs['pk']
        instancia_nivel = self.model.objects.get(id=id_nivel)
        form = self.form_class(request.POST, instance=instancia_nivel)

        if form.is_valid():
            form.save()
            UpdatePrimerNivel(id_nivel, request.POST['descripcion_nivel'])
            request.session['message_class'] = "alert alert-success"
            messages.success(self.request, "Los datos fueron actualizados correctamente!")
            return HttpResponseRedirect('/estructura/listar/1')
        else:
            request.session['message_class'] = "alert alert-danger"
            messages.error(self.request, "Error interno: No se ha eliminado el registro. Comuníquese con el administrador.")
            return HttpResponseRedirect('/estructura/listar/1')

############ FIN GESTIÓN PRIMER NIVEL##########################

############GESTIÓN SEGUNDO NIVEL##########################
def CreaSegundoNivel(descripcion_nivel,  periodo_activo):
    Ges_Niveles.objects.create(
        orden_nivel=2,
        descripcion_nivel=descripcion_nivel,
        estado=1,
        id_segundo_nivel=Ges_SegundoNivel.objects.latest('id'),
        id_periodo= periodo_activo,
    )
    return None

def UpdateSegundoNivel(id_segundo_nivel, descripcion_nivel):
    IdSegundo = Ges_Niveles.objects.get(Q(id_segundo_nivel=id_segundo_nivel) & Q(orden_nivel=2))
    Ges_Niveles.objects.filter(id=IdSegundo.id).update(
        descripcion_nivel=descripcion_nivel,

    )
    return None

def DeleteSegundoNivel(id_segundo_nivel):
    IdSegundo = Ges_Niveles.objects.get(Q(id_segundo_nivel=id_segundo_nivel) & Q(orden_nivel=2))
    Ges_Niveles.objects.filter(id=IdSegundo.id).delete()
    return None



class SegundoNivelList(ListView):
    model = Ges_SegundoNivel
    template_name = 'estructura/estructura_list_sn.html'

    def get_context_data(self, **kwargs):
        context = super(SegundoNivelList, self).get_context_data(**kwargs)

        try:
            periodo_actual = Glo_Periodos.objects.get(id_estado=1)
        except Glo_Periodos.DoesNotExist:
            return None

        lista_horas = Ges_SegundoNivel.objects.filter(id_periodo=periodo_actual.id)
        context['object_list'] = lista_horas
        return context


    #def get_context_data(self,  **kwargs):
        #context = super(SegundoNivelList, self).get_context_data(**kwargs)
        #lista_objetivos = Ges_SegundoNivel.objects.all() #queryset original que trae el listado completo pero intenté traer la cantidad de objetivos y utilicé el queryJoin.

        # La queryJoin funciona pero pierde la relación del FK con el primer nivel hay que revisar ya que existen alternativas de solucion, por otro lado no se aún como agregar una tercera
        #tabla por lo cual utilicé el raw, al parecer no es la mejor práctica pero funciona para sacar de apuros NO ABUSAR de este recurso.

        #queryJoin = Ges_SegundoNivel.objects.values('id','descripcion_nivel', 'primer_nivel', 'define_actividad', 'ges_objetivo_tactico__id_segundo_nivel').annotate(Count('id'))

        #consultaRaw= Ges_SegundoNivel.objects.raw('SELECT E.id, E.descripcion_nivel, P.descripcion_nivel  , E.define_actividad ,COUNT( O.id) AS Cantidad_Objetivos '
                                              # ' from estructura_ges_segundonivel E , objetivos_ges_objetivo_tactico O, estructura_ges_primernivel P '
                                               #'WHERE E.id=O.id_segundo_nivel_id AND P.id=E.primer_nivel_id GROUP BY E.descripcion_nivel')
        #context['object_list'] = consultaRaw
        #return context

class SegundoNivelCreate(SuccessMessageMixin, CreateView ):
    form_class = SegundoNivelForm

    template_name = 'estructura/estructura_form_sn.html'


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
            CreaSegundoNivel(request.POST['descripcion_nivel'], periodo_activo)
            request.session['message_class'] = "alert alert-success"
            messages.success(self.request, "Los datos fueron creados correctamente!")
            return HttpResponseRedirect('/estructura/listar/2')
        else:
            request.session['message_class'] = "alert alert-danger"
            messages.error(self.request, "Error interno: No se ha creado el registro. Comuníquese con el administrador.")
            return HttpResponseRedirect('/estructura/listar/2')


class SegundoNivelUpdate(SuccessMessageMixin, UpdateView ):
    model = Ges_SegundoNivel
    form_class = SegundoNivelForm
    template_name = 'estructura/estructura_form_sn.html'

    def post(self, request, *args, **kwargs):

        self.object = self.get_object
        id_nivel = kwargs['pk']
        instancia_nivel = self.model.objects.get(id=id_nivel)
        form = self.form_class(request.POST, instance=instancia_nivel)

        if form.is_valid():
            form.save()
            UpdateSegundoNivel(id_nivel, request.POST['descripcion_nivel'])
            request.session['message_class'] = "alert alert-success"
            messages.success(self.request, "Los datos fueron actualizados correctamente!" )
            return HttpResponseRedirect('/estructura/listar/2')
        else:
            request.session['message_class'] = "alert alert-danger"
            messages.error(self.request, "Error interno: No se ha actualizado el registro. Comuníquese con el administrador.")
            return HttpResponseRedirect('/estructura/listar/2')


class SegundoNivelDelete(SuccessMessageMixin, DeleteView ):
    model = Ges_SegundoNivel
    template_name = 'estructura/estructura_delete_sn.html'


    def delete(self, request, *args, **kwargs):
        id_nivel = kwargs['pk']
        obj = self.get_object()
        try:
            DeleteSegundoNivel(id_nivel)
            obj.delete()

            request.session['message_class'] = "alert alert-success"
            messages.success(self.request, "El registro fue eliminado correctamente!")
            return HttpResponseRedirect('/estructura/listar/2')

        except ProtectedError as e:
            request.session['message_class'] = "alert alert-warning"
            messages.error(request, "Alerta de integridad: Este nivel posee subniveles  u objetivos asociados  los que deben ser borrados antes de borrar este nivel.")
            return HttpResponseRedirect('/estructura/listar/2')

        except Exception  as e:
            request.session['message_class'] = "alert alert-danger"
            messages.error(request, "Error interno: No se ha eliminado el registro. Comuníquese con el administrador.")
            return HttpResponseRedirect('/estructura/listar/2')

############ FIN GESTIÓN SEGUNDO NIVEL##########################

############ GESTIÓN TERCER NIVEL##########################
def CreaTercerNivel(descripcion_nivel,  periodo_activo):
    Ges_Niveles.objects.create(
        orden_nivel=3,
        descripcion_nivel=descripcion_nivel,
        estado=1,
        id_tercer_nivel=Ges_TercerNivel.objects.latest('id'),
        id_periodo=periodo_activo,
    )
    return None

def UpdateTercerNivel(id_tercer_nivel, descripcion_nivel):
    IdTercer= Ges_Niveles.objects.get(Q(id_tercer_nivel=id_tercer_nivel) & Q(orden_nivel=3))
    Ges_Niveles.objects.filter(id=IdTercer.id).update(
        descripcion_nivel=descripcion_nivel,

    )
    return None

def DeleteTercerNivel(id_tercer_nivel):
    IdTercer = Ges_Niveles.objects.get(Q(id_tercer_nivel=id_tercer_nivel) & Q(orden_nivel=3))
    Ges_Niveles.objects.filter(id=IdTercer.id).delete()
    return None



class TercerNivelList(ListView):
    model = Ges_TercerNivel
    template_name = 'estructura/estructura_list_tn.html'

    def get_context_data(self, **kwargs):
        context = super(TercerNivelList, self).get_context_data(**kwargs)

        try:
            periodo_actual = Glo_Periodos.objects.get(id_estado=1)
        except Glo_Periodos.DoesNotExist:
            return None

        lista_horas = Ges_TercerNivel.objects.filter(id_periodo=periodo_actual.id)
        context['object_list'] = lista_horas
        return context

class TercerNivelCreate(SuccessMessageMixin, CreateView ):
    form_class = TercerNivelForm
    template_name = 'estructura/estructura_form_tn.html'

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
            CreaTercerNivel(request.POST['descripcion_nivel'], periodo_activo)
            request.session['message_class'] = "alert alert-success"
            messages.success(self.request, "Los datos fueron creados correctamente!")
            return HttpResponseRedirect('/estructura/listar/3')
        else:
            request.session['message_class'] = "alert alert-danger"
            messages.error(self.request, "Error interno: No se ha creado el registro. Comuníquese con el administrador.")
            return HttpResponseRedirect('/estructura/listar/3')


class TercerNivelUpdate(SuccessMessageMixin, UpdateView ):
    model = Ges_TercerNivel
    form_class = TercerNivelForm
    template_name = 'estructura/estructura_form_tn.html'


    def post(self, request, *args, **kwargs):

        self.object = self.get_object
        id_nivel = kwargs['pk']
        instancia_nivel = self.model.objects.get(id=id_nivel)
        form = self.form_class(request.POST, instance=instancia_nivel)

        if form.is_valid():
            form.save()
            UpdateTercerNivel(id_nivel, request.POST['descripcion_nivel'])
            request.session['message_class'] = "alert alert-success"
            messages.success(self.request, "Los datos fueron actualizados correctamente!")
            return HttpResponseRedirect('/estructura/listar/3')
        else:
            request.session['message_class'] = "alert alert-danger"
            messages.error(self.request, "Error interno: No se ha actualizado el registro. Comuníquese con el administrador.")
            return HttpResponseRedirect('/estructura/listar/3')

class TercerNivelDelete(SuccessMessageMixin, DeleteView ):
    model = Ges_TercerNivel
    template_name = 'estructura/estructura_delete_tn.html'


    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        id_nivel = kwargs['pk']
        try:
            DeleteTercerNivel(id_nivel)
            obj.delete()
            request.session['message_class'] = "alert alert-success"
            messages.success(self.request, "El registro fue eliminado correctamente!")
            return HttpResponseRedirect('/estructura/listar/3')

        except ProtectedError as e:
            request.session['message_class'] = "alert alert-warning"
            messages.error(request, "Alerta de integridad: Este nivel posee subniveles  u objetivos asociados  los que deben ser borrados antes de borrar este nivel.")
            return HttpResponseRedirect('/estructura/listar/3')

        except Exception  as e:
            request.session['message_class'] = "alert alert-danger"
            messages.error(request, "Error interno: No se ha eliminado el registro. Comuníquese con el administrador.")
            return HttpResponseRedirect('/estructura/listar/3')

############ FIN GESTIÓN TERCER NIVEL##########################

############ GESTIÓN CUARTO NIVEL##########################

def CreaCuartoNivel(descripcion_nivel,  periodo_activo):
    Ges_Niveles.objects.create(
        orden_nivel=4,
        descripcion_nivel=descripcion_nivel,
        estado=1,
        id_cuarto_nivel=Ges_CuartoNivel.objects.latest('id'),
        id_periodo=periodo_activo,
    )
    return None

def UpdateCuartoNivel(id_cuarto_nivel, descripcion_nivel):
    IdCuarto= Ges_Niveles.objects.get(Q(id_cuarto_nivel=id_cuarto_nivel) & Q(orden_nivel=4))
    Ges_Niveles.objects.filter(id=IdCuarto.id).update(
        descripcion_nivel=descripcion_nivel,

    )
    return None

def DeleteCuartoNivel(id_cuarto_nivel):
    IdCuarto = Ges_Niveles.objects.get(Q(id_cuarto_nivel=id_cuarto_nivel) & Q(orden_nivel=4))
    Ges_Niveles.objects.filter(id=IdCuarto.id).delete()
    return None


class CuartoNivelList(ListView):
    model = Ges_CuartoNivel
    template_name = 'estructura/estructura_list_cn.html'

    def get_context_data(self, **kwargs):
        context = super(CuartoNivelList, self).get_context_data(**kwargs)

        try:
            periodo_actual = Glo_Periodos.objects.get(id_estado=1)
        except Glo_Periodos.DoesNotExist:
            return None

        lista_horas = Ges_CuartoNivel.objects.filter(id_periodo=periodo_actual.id)
        context['object_list'] = lista_horas
        return context


class CuartoNivelCreate(SuccessMessageMixin, CreateView ):
    form_class = CuartoNivelForm
    template_name = 'estructura/estructura_form_cn.html'

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
            CreaCuartoNivel(request.POST['descripcion_nivel'], periodo_activo)
            request.session['message_class'] = "alert alert-success"
            messages.success(self.request, "Los datos fueron creados correctamente!")
            return HttpResponseRedirect('/estructura/listar/4')
        else:
            request.session['message_class'] = "alert alert-danger"
            messages.error(self.request, "Error interno: No se ha creado el registro. Comuníquese con el administrador.")
            return HttpResponseRedirect('/estructura/listar/4')



class CuartoNivelUpdate(SuccessMessageMixin, UpdateView ):
    model = Ges_CuartoNivel
    form_class = CuartoNivelForm
    template_name = 'estructura/estructura_form_cn.html'

    def post(self, request, *args, **kwargs):

        self.object = self.get_object
        id_nivel = kwargs['pk']
        instancia_nivel = self.model.objects.get(id=id_nivel)
        form = self.form_class(request.POST, instance=instancia_nivel)

        if form.is_valid():
            form.save()
            UpdateCuartoNivel(id_nivel, request.POST['descripcion_nivel'])
            request.session['message_class'] = "alert alert-success"
            messages.success(self.request, "Los datos fueron actualizados correctamente!")
            return HttpResponseRedirect('/estructura/listar/4')
        else:
            request.session['message_class'] = "alert alert-danger"
            messages.error(self.request, "Error interno: No se ha actualizado el registro. Comuníquese con el administrador.")
            return HttpResponseRedirect('/estructura/listar/4')


class CuartoNivelDelete(SuccessMessageMixin, DeleteView ):
    model = Ges_CuartoNivel
    template_name = 'estructura/estructura_delete_cn.html'


    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        id_nivel = kwargs['pk']
        try:
            DeleteCuartoNivel(id_nivel)
            obj.delete()
            request.session['message_class'] = "alert alert-success"
            messages.success(self.request, "El registro fue eliminado correctamente!")
            return HttpResponseRedirect('/estructura/listar/4')

        except ProtectedError as e:
            request.session['message_class'] = "alert alert-warning"
            messages.error(request, "Alerta de integridad: Este nivel posee subniveles u objetivos asociados los que deben ser borrados antes de borrar este nivel.")
            return HttpResponseRedirect('/estructura/listar/4')

        except Exception  as e:
            request.session['message_class'] = "alert alert-danger"
            messages.error(request, "Error interno: No se ha eliminado el registro. Comuníquese con el administrador.")
            return HttpResponseRedirect('/estructura/listar/4')

############ FIN GESTIÓN CUARTO NIVEL##########################







