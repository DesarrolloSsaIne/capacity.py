from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from apps.periodos.forms import periodosForm, Seguimiento_cierreform
from apps.periodos.models import Glo_Periodos, Glo_Seguimiento
from apps.controlador.models import Ges_Controlador
from apps.estado_seguimiento.models import Glo_EstadoSeguimiento

from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.db.models.deletion import ProtectedError
from django.core.mail import EmailMessage
from datetime import date
from datetime import datetime
# Create your views here.


class PeriodosList(ListView):
    model = Glo_Periodos
    template_name = 'periodos/periodo_list.html'


class PeriodosCreate(SuccessMessageMixin, CreateView):
    model = Glo_Periodos
    form_class = periodosForm
    template_name = 'periodos/periodo_form.html'


    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        if form.is_valid():
            form.instance.fecha_inicio= date.today()
            form.save()
            request.session['message_class'] = "alert alert-success"
            messages.success(self.request, "Los datos fueron creados correctamente!")
            return HttpResponseRedirect('/periodos/listar')
        else:
            request.session['message_class'] = "alert alert-danger"
            messages.error(self.request, "Error interno: No se ha creado el registro. Comuníquese con el administrador.")
            return HttpResponseRedirect('/periodos/listar')



class PeriodosEdit(SuccessMessageMixin, UpdateView ):
    model = Glo_Periodos
    form_class = periodosForm
    template_name = 'periodos/periodo_form.html'

    def post(self, request, *args, **kwargs):

        self.object = self.get_object
        id_periodo = kwargs['pk']
        instancia_nivel = self.model.objects.get(id=id_periodo)
        form = self.form_class(request.POST, instance=instancia_nivel)

        if form.is_valid():
            form.save()
            request.session['message_class'] = "alert alert-success"
            messages.success(self.request, "Los datos fueron actualizados correctamente!" )
            return HttpResponseRedirect('/periodos/listar')
        else:
            request.session['message_class'] = "alert alert-danger"
            messages.error(self.request, "Error interno: No se ha actualizado el registro. Comuníquese con el administrador.")
            return HttpResponseRedirect('/periodos/listar')


class PeriodosDelete(SuccessMessageMixin, DeleteView ):
    model = Glo_Periodos
    template_name = 'periodos/periodo_delete.html'

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        try:
            obj.delete()
            request.session['message_class'] = "alert alert-success"
            messages.success(self.request, "El registro fue eliminado correctamente!")
            return HttpResponseRedirect('/periodos/listar')

        except ProtectedError as e:
            request.session['message_class'] = "alert alert-danger"
            messages.error(request, "Error de integridad: Este nivel posee subniveles los que deben ser borrados antes de borrar este nivel.")
            return HttpResponseRedirect('/periodos/listar')

        except Exception  as e:
            request.session['message_class'] = "alert alert-danger"
            messages.error(request, "Error interno: No se ha eliminado el registro. Comuníquese con el administrador.")
            return HttpResponseRedirect('/periodos/listar')




class SeguimientoList(ListView):
    model = Glo_Seguimiento
    template_name = 'periodos/seguimiento_list.html'



    def get_context_data(self, **kwargs):
        context = super(SeguimientoList, self).get_context_data(**kwargs)
        #id_usuario_actual = self.request.user.id  # obtiene id usuario actual
        self.request.session['id_periodo']=self.kwargs['pk'] #guarda id  controlador


        queryset= Glo_Seguimiento.objects.filter(id_periodo=self.kwargs['pk'])


        context['object_list'] = queryset
        context['periodo'] = PeriodoActual()




        return context


class SeguimientoCerrarPeriodo(UpdateView):
    model = Glo_Seguimiento
    template_name = 'periodos/seguimiento_cerrar.html'
    form_class = Seguimiento_cierreform

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        pk = kwargs['pk']
        instancia = self.model.objects.get(id=pk)
        form = self.form_class(request.POST, instance=instancia)

        id_nuevo_estado= Glo_EstadoSeguimiento.objects.get(id=2)

        id_periodo=self.request.session['id_periodo']

        if form.is_valid():

            form.instance.id_estado_seguimiento=id_nuevo_estado
            form.instance.fecha_termino= date.today()

            form.save()

            try:

                EnviarCorreoCierre()

                request.session['message_class'] = "alert alert-success"  # Tipo mensaje
                messages.success(request, "La etapa de seguimiento fue cerrada y se le ha enviado un correo a las jefaturas que formulan.!")  # mensaje
                return HttpResponseRedirect('/periodos/listar_seguimiento/' + str(id_periodo))  # Redirije a la pantalla principal

            except:

                 request.session['message_class'] = "alert alert-warning" #Tipo mensaje
                 messages.success(request, "La etapa de seguimiento fue cerrada correctamente!, pero el servicio de correo tuvo un inconveniente favor comuníquese con las jefaturas que formulan para informar el cierre de esta etapa.") # mensaje
                 return HttpResponseRedirect('/periodos/listar_seguimiento/' + str(id_periodo)) # Redirije a la pantalla principal

        else:

            request.session['message_class'] = "alert alert-danger"
            messages.error(self.request, "Error interno: No se ha cerrado la etapa de seguimiento. Comuníquese con el administrador.")
            return HttpResponseRedirect('/periodos/listar_seguimiento' + str(id_periodo))



class SeguimientoAbrirPeriodo(SuccessMessageMixin, CreateView):
    model = Glo_Seguimiento
    template_name = 'periodos/seguimiento_abrir.html'
    form_class = Seguimiento_cierreform


    def get_context_data(self, **kwargs):
        context = super(SeguimientoAbrirPeriodo, self).get_context_data(**kwargs)

        try:
             estado= Glo_Seguimiento.objects.get(id_estado_seguimiento=1)
        except Glo_Seguimiento.DoesNotExist:
             estado = 0

        context["estado_seguimiento"] = estado
        return context

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        id_nuevo_estado= Glo_EstadoSeguimiento.objects.get(id=1)
        periodo_actual = Glo_Periodos.objects.get(id_estado=1)

        id_periodo=self.request.session['id_periodo']

        if form.is_valid():
            form.instance.id_periodo= periodo_actual
            form.instance.id_estado_seguimiento=id_nuevo_estado
            form.instance.fecha_inicio= date.today()

            form.save()

            try:

                EnviarCorreoAbrir()

                request.session['message_class'] = "alert alert-success"  # Tipo mensaje
                messages.success(request, "El periodo de seguimiento fue abierto correctamente! y se ha enviado un correo al analista!")  # mensaje
                return HttpResponseRedirect('/periodos/listar_seguimiento/' + str(id_periodo))  # Redirije a la pantalla principal

            except:

                 request.session['message_class'] = "alert alert-warning" #Tipo mensaje
                 messages.success(request, "El periodo de seguimiento fue abierto correctamente!, pero el servicio de correo tuvo un inconveniente favor comuníquese con la jefatura directa para informar de la apertura.") # mensaje
                 return HttpResponseRedirect('/periodos/listar_seguimiento/' + str(id_periodo)) # Redirije a la pantalla principal

        else:

            request.session['message_class'] = "alert alert-danger"
            messages.error(self.request, "Error interno: No se ha abierto la etapa de seguimiento. Comuníquese con el administrador.")
            return HttpResponseRedirect('/periodos/listar_seguimiento' + str(id_periodo))




def PeriodoActual():
    try:
        periodo_actual = Glo_Periodos.objects.get(id_estado=1)
    except Glo_Periodos.DoesNotExist:
        return None
    return periodo_actual


def EnviarCorreoCierre():
    controladorPlan = Ges_Controlador.objects.filter(id_periodo=PeriodoActual())

    for controladorPlan in controladorPlan:

        usuario=  str(controladorPlan.analista_asignado)
        ahora = datetime.now()
        fecha = ahora.strftime("%d" + " de " + "%B" + " de " + "%Y" + " a las " + "%H:%M")


        # Envío al analista
        email_jefatura_ingresaAct = controladorPlan.analista_asignado.email
        idcorreoJefatura = [email_jefatura_ingresaAct]
        subject = 'Cierre etapa Seguimiento'
        messageHtml = 'Estimada(o) <b>' + usuario + '</b> ,<br> Con fecha  '+ str(fecha) +', le informamos que el proceso de seguimiento ha sido cerrado. <br><p style="font-size:12px;color:red;">correo generado automaticamente favor no responder.'

        email = EmailMessage(subject, messageHtml ,to=[idcorreoJefatura])
        email.content_subtype='html'
        email.send()

def EnviarCorreoAbrir():
    controladorPlan = Ges_Controlador.objects.filter(id_periodo=PeriodoActual())

    for controladorPlan in controladorPlan:

        usuario=  str(controladorPlan.analista_asignado)
        ahora = datetime.now()
        fecha = ahora.strftime("%d" + " de " + "%B" + " de " + "%Y" + " a las " + "%H:%M")


        # Envío al analista
        email_jefatura_ingresaAct = controladorPlan.analista_asignado.email
        idcorreoJefatura = [email_jefatura_ingresaAct]
        subject = 'Apertura etapa Seguimiento'
        messageHtml = 'Estimada(o) <b>' + usuario + '</b> ,<br> Con fecha  '+ str(fecha) +', le informamos que el proceso de seguimiento ha sido abierto. <br><p style="font-size:12px;color:red;">correo generado automaticamente favor no responder.'

        email = EmailMessage(subject, messageHtml ,to=[idcorreoJefatura])
        email.content_subtype='html'
        email.send()