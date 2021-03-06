from django.shortcuts import render

from apps.controlador.models import Ges_Controlador
from apps.estado_flujo.models import Glo_EstadoFlujo
from apps.planificacion_admin.forms import Planificacion_adminForm
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from apps.registration.models import logEventos
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.db.models import Q
from apps.estructura.models import Ges_Niveles, Ges_CuartoNivel, Ges_TercerNivel, Ges_SegundoNivel, Ges_PrimerNivel
from apps.jefaturas.models import Ges_Jefatura
from apps.periodos.models import Glo_Seguimiento
from django.core.mail import EmailMessage
from apps.periodos.models import Glo_Periodos


def usuarioActual(request):

    id_usuario_actual = request.user.id  # obtiene id usuario actual
    return id_usuario_actual


class PlanificacionAdminList(ListView):
    model = Ges_Controlador
    template_name = 'planificacion_admin/planificacion_admin_list.html'

    def get_context_data(self, **kwargs):
        context = super(PlanificacionAdminList, self).get_context_data(**kwargs)

        try:
            periodo_actual = Glo_Periodos.objects.get(id_estado=1)
        except Glo_Periodos.DoesNotExist:
            return None



        queryset = Ges_Controlador.objects.filter((Q(estado_flujo_id=10) | Q(estado_flujo_id=11) | Q(estado_flujo_id=6)) & Q(id_periodo=periodo_actual))

        context['object_list'] = queryset

        return context

class AsignaAnalista(UpdateView):
    model = Ges_Controlador
    template_name = 'planificacion_admin/planificacion_admin_asigna.html'
    form_class = Planificacion_adminForm

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        pk = kwargs['pk']
        instancia = self.model.objects.get(id=pk)
        form = self.form_class(request.POST, instance=instancia)

        try:
            periodo_actual = Glo_Periodos.objects.get(id_estado=1)
        except Glo_Periodos.DoesNotExist:
            return None

        id_nuevo_estado= Glo_EstadoFlujo.objects.get(id=6)

        if form.is_valid():

            form.instance.estado_flujo=id_nuevo_estado

            form.save()

            try:

                controladorPlan = Ges_Controlador.objects.get(Q(id=pk) & Q(id_periodo=periodo_actual))
                usuario=  str(controladorPlan.analista_asignado)
                unidad_plan=str(controladorPlan.id_jefatura.id_nivel)
                jefe_elabora= str(controladorPlan.id_jefatura.id_user)


                # Env??o al analista
                email_jefatura_ingresaAct = controladorPlan.analista_asignado.email
                idcorreoJefatura = [email_jefatura_ingresaAct]
                subject = 'Asignaci??n de Plan'
                messageHtml = 'Estimada(o) <b>' + usuario + '</b> ,<br> El administrador de Planificaci??n le ha asignado un PLAN para su revisi??n con los siguientes antecedentes:.<br> <br> Unidad Plan: <b>'+ unidad_plan +'</b> <br>Jefatura Elabora: <b>'+ jefe_elabora  + '</b> <br><br> Para su revisi??n ingrese al sistema Capacity Institucional y dir??jase a su bandeja de entrada. <br> Atte. <br><br>Subdpto. de Planificaci??n Institucional.<br><p style="font-size:12px;color:red;">correo generado automaticamente favor no responder.'

                email = EmailMessage(subject, messageHtml ,to=[idcorreoJefatura])
                email.content_subtype='html'
                email.send()

                request.session['message_class'] = "alert alert-success"  # Tipo mensaje
                messages.success(request, "El plan fue asignado correctamente y se ha enviado un correo al analista!")  # mensaje
                return HttpResponseRedirect('/planificacion_admin/listar/')  # Redirije a la pantalla principal

            except:

                 request.session['message_class'] = "alert alert-warning" #Tipo mensaje
                 messages.success(request, "El plan fue asignado correctamente!, pero el servicio de correo tuvo un inconveniente favor comun??quese con el analista para informar la asignaci??n.") # mensaje
                 return HttpResponseRedirect('/planificacion_admin/listar/') # Redirije a la pantalla principal

        else:

            request.session['message_class'] = "alert alert-danger"
            messages.error(self.request, "Error interno: No se ha asignado el funcionario. Comun??quese con el administrador.")
            return HttpResponseRedirect('/planificacion_admin/listar/')


class PlanificacionAdminUnidadesList(ListView): #Modificado por JR- sprint 10
    model = Ges_Niveles
    template_name = 'planificacion_admin/planificacion_admin_plan_list.html'

    def get_context_data(self, **kwargs):
        context = super(PlanificacionAdminUnidadesList, self).get_context_data(**kwargs)
        id_usuario_actual = self.request.user.id  # obtiene id usuario actual

        try:
            periodo_actual = Glo_Periodos.objects.get(id_estado=1)
        except Glo_Periodos.DoesNotExist:
            return None

        # try:
        #     periodo_actual = Glo_Periodos.objects.get(id_estado=1)
        # except Glo_Periodos.DoesNotExist:
        #     return None

        # id_jefatura = Ges_Jefatura.objects.get(id_user=id_usuario_actual)

        id_controlador = Ges_Controlador.objects.filter(id_periodo=periodo_actual)

        try:
             estado= Glo_Seguimiento.objects.get(Q(id_estado_seguimiento=1) & Q(id_periodo=periodo_actual))
        except Glo_Seguimiento.DoesNotExist:
             estado = 0

        context['estado_seguimiento'] = estado
        context['object_list'] = id_controlador

        return context





def logEventosCreate(tipo_evento, metodo ,usuario_evento, jefatura_dirigida):
    logEventos.objects.create(
        tipo_evento=tipo_evento,
        metodo=metodo,
        usuario_evento=usuario_evento,
        jefatura_dirigida=jefatura_dirigida,
    )
    return None