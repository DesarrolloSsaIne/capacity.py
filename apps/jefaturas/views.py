from django.shortcuts import render
from apps.jefaturas.models import Ges_Jefatura
from apps.jefaturas.forms import JefaturasForm,JefaturasFormUpdate
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.db.models.deletion import ProtectedError
from apps.periodos.models import Glo_Periodos
from django.contrib.auth.models import User, Group
# Create your views here.


class JefaturaList(ListView):
    model = Ges_Jefatura
    template_name = 'jefaturas/jefatura_list.html'

    def get_context_data(self, **kwargs):
        context = super(JefaturaList, self).get_context_data(**kwargs)

        try:
            periodo_actual = Glo_Periodos.objects.get(id_estado=1)
        except Glo_Periodos.DoesNotExist:
            return None

        lista_horas = Ges_Jefatura.objects.filter(id_periodo=periodo_actual.id)
        context['object_list'] = lista_horas
        return context


class JefaturaCreate(SuccessMessageMixin, CreateView ):
    form_class = JefaturasForm
    template_name = 'jefaturas/jefaturas_form.html'


    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        usuario_ingreso= request.POST['id_user']
        nivel_ingreso = request.POST['id_nivel']
        usuario_registrado= Ges_Jefatura.objects.filter(id_user=usuario_ingreso)
        nivel_ingreso=Ges_Jefatura.objects.filter(id_nivel=nivel_ingreso)

        try:
            periodo_activo = Glo_Periodos.objects.get(id_estado=1)
        except Glo_Periodos.DoesNotExist:
            return None

        if form.is_valid():

            if usuario_registrado:
                request.session['message_class'] = "alert alert-danger"
                messages.error(self.request,
                               "Error interno: El usuario que intenta registrar ya posee una jefatura asociada, vuelva a intentarlo.")
                return HttpResponseRedirect('/jefaturas/listar/')
            else:
                if nivel_ingreso:
                    request.session['message_class'] = "alert alert-danger"
                    messages.error(self.request,
                                   "Error interno: El nivel que desea agregar ya se encuentra registrado, vuelva a intentarlo. ")
                    return HttpResponseRedirect('/jefaturas/listar/')
                else:

                    form.instance.id_periodo = periodo_activo
                    form.save()
                    request.session['message_class'] = "alert alert-success"
                    messages.success(self.request, "Los datos fueron creados correctamente!")
                    return HttpResponseRedirect('/jefaturas/listar/')
        else:
            request.session['message_class'] = "alert alert-danger"
            messages.error(self.request, "Error interno: No se ha creado el registro. Comuníquese con el administrador.")
            return HttpResponseRedirect('/jefaturas/listar/')


class JefaturaDelete(SuccessMessageMixin, DeleteView ):
    model = Ges_Jefatura
    template_name = 'jefaturas/jefatura_delete.html'

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        try:
            obj.delete()


            request.session['message_class'] = "alert alert-success"
            messages.success(self.request, "El registro fue eliminado correctamente!")
            return HttpResponseRedirect('/jefaturas/listar/')

        except ProtectedError as e:
            request.session['message_class'] = "alert alert-danger"
            messages.error(request, "Error de integridad: Este nivel posee subniveles los que deben ser borrados antes de borrar este nivel.")
            return HttpResponseRedirect('/jefaturas/listar/')

        except Exception  as e:
            request.session['message_class'] = "alert alert-danger"
            messages.error(request, "Error interno: No se ha eliminado el registro. Comuníquese con el administrador.")
            return HttpResponseRedirect('/jefaturas/listar/')


class JefaturaUpdate(UpdateView):
    model = Ges_Jefatura
    form_class = JefaturasFormUpdate
    template_name = 'jefaturas/jefaturas_form.html'


    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        id_nivel = kwargs['pk']
        instancia_nivel = self.model.objects.get(id=id_nivel)
        form = self.form_class(request.POST, instance=instancia_nivel)
        usuario_ingreso= request.POST['id_user'] #Usuario que entra
        nivel_ingreso = request.POST['id_nivel']
        #usuario_registrado= Ges_Jefatura.objects.filter(id_user=usuario_ingreso)
        #nivel_ingreso=Ges_Jefatura.objects.filter(id_nivel=nivel_ingreso)



        try:
            usuario_id =  Ges_Jefatura.objects.values('id_user').get(id_user=usuario_ingreso)['id_user']
        except Ges_Jefatura.DoesNotExist:
            usuario_id = None


        try:
            usuario_id_sale =  Ges_Jefatura.objects.values('id_user').get(id=id_nivel)['id_user'] #Usuario que sale
        except Ges_Jefatura.DoesNotExist:
            usuario_id_sale = None

        try:
            nivel_id = Ges_Jefatura.objects.values('id_nivel').get(id_nivel=nivel_ingreso)['id_nivel']
        except Ges_Jefatura.DoesNotExist:
            nivel_id = None


        usuario = Ges_Jefatura.objects.filter(id_user=usuario_ingreso).count()

        if form.is_valid():
            if usuario != 0 and usuario_ingreso==str(usuario_id) and nivel_ingreso==str(nivel_id):
                request.session['message_class'] = "alert alert-warning"
                messages.error(self.request,
                               "Atención: El usuario que intenta registrar ya posee una jefatura asociada. No se generaron cambios.")
                return HttpResponseRedirect('/jefaturas/listar/')
            else:

                CambioPerfilJefatura(usuario_id_sale,usuario_ingreso)
                form.save()



                request.session['message_class'] = "alert alert-success"
                messages.success(self.request, "Los datos fueron actualizados correctamente!")
                return HttpResponseRedirect('/jefaturas/listar/')
        else:
            request.session['message_class'] = "alert alert-danger"
            messages.error(self.request, "Error interno: No se ha actualizad el registro. Comuníquese con el administrador.")
            return HttpResponseRedirect('/jefaturas/listar/')


def CambioPerfilJefatura(user_sale, user_entra):


    g = Group.objects.get(user=user_sale)

    g.user_set.add(user_entra)
    g.user_set.remove(user_sale)
