from django.shortcuts import render
from apps.controlador.models import Ges_Controlador
from apps.estado_flujo.models import Glo_EstadoFlujo
from apps.planificacion_admin.forms import Planificacion_adminForm
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from apps.periodos.models import Glo_Periodos
from django.contrib.auth.models import User, Group
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.db.models import Q
from django.core import mail
from django.conf import settings
from django.utils.module_loading import import_string
from django.core.mail import EmailMultiAlternatives, send_mail


# Generic Functions of projects.
def PeriodoActual():
    try:
        periodo_actual = Glo_Periodos.objects.get(id_estado=1)
    except Glo_Periodos.DoesNotExist:
        return None
    return periodo_actual

def usuarioActual(request):

    id_usuario_actual = request.user.id  # obtiene id usuario actual
    return id_usuario_actual


class PlanificacionAdminList(ListView):
    model = Ges_Controlador
    template_name = 'planificacion_admin/planificacion_admin_list.html'
    context_object_name = 'object_list'
    queryset = Ges_Controlador.objects.filter((Q(estado_flujo_id=10) | Q(estado_flujo_id=11) | Q(estado_flujo_id=6)) & Q(id_periodo=PeriodoActual()))


class AsignaAnalista(UpdateView):
    model = Ges_Controlador
    template_name = 'planificacion_admin/planificacion_admin_asigna.html'
    form_class = Planificacion_adminForm

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        pk = kwargs['pk']
        instancia = self.model.objects.get(id=pk)
        form = self.form_class(request.POST, instance=instancia)

        id_nuevo_estado= Glo_EstadoFlujo.objects.get(id=6)

        if form.is_valid():

            form.instance.estado_flujo=id_nuevo_estado

            form.save()

            try:

                controladorPlan = Ges_Controlador.objects.get(Q(id=pk) & Q(id_periodo=PeriodoActual()))
                usuario=  str(controladorPlan.analista_asignado)
                unidad_plan=str(controladorPlan.id_jefatura.id_nivel)
                jefe_elabora= str(controladorPlan.id_jefatura.id_user)


                # Envío al analista
                email_jefatura_ingresaAct = controladorPlan.analista_asignado.email
                idcorreoJefatura = [email_jefatura_ingresaAct]
                subject = 'Asignación de Plan'
                messageHtml = 'Estimada(o) <b>' + usuario + '</b> ,<br> El administrador de Planificación le ha asignado un PLAN para su revisión con los siguientes antecedentes:.<br> <br> Unidad Plan: <b>'+ unidad_plan +'</b> <br>Jefatura Elabora: <b>'+ jefe_elabora  + '</b> <br><br> Para su revisión ingrese al sistema Capacity Institucional y diríjase a su bandeja de entrada. <br> Atte. <br><br>Subdpto. de Planificación Institucional.<br><p style="font-size:12px;color:red;">correo generado automaticamente favor no responder.'
                send_correo(idcorreoJefatura, subject, messageHtml)

                request.session['message_class'] = "alert alert-success"  # Tipo mensaje
                messages.success(request, "El plan fue asignado correctamente y se ha enviado un correo al analista!")  # mensaje
                return HttpResponseRedirect('/planificacion_admin/listar/')  # Redirije a la pantalla principal

            except:

                request.session['message_class'] = "alert alert-warning" #Tipo mensaje
                messages.success(request, "El plan fue asignado correctamente!, pero el servicio de correo tuvo un inconveniente favor comuníquese con el analista para informar la asignación.") # mensaje
                return HttpResponseRedirect('/planificacion_admin/listar/') # Redirije a la pantalla principal

        else:

            request.session['message_class'] = "alert alert-danger"
            messages.error(self.request, "Error interno: No se ha asignado el funcionario. Comuníquese con el administrador.")
            return HttpResponseRedirect('/planificacion_admin/listar/')





def get_connection(backend=None, fail_silently=False, **kwds):
    klass = import_string(backend or settings.EMAIL_BACKEND)
    return klass(fail_silently=fail_silently, **kwds)

def send_correo(email, subject,  messageHtml):
    email = email
    subject = subject
    from_email = settings.EMAIL_HOST_USER
    email_messages = []
    subject, from_email, to = subject, from_email, email
    html_content = messageHtml
    fail_silently = False
    auth_user = None
    auth_password = None
    connection = None

    connection = connection or get_connection(
        username=auth_user,
        password=auth_password,
        fail_silently=fail_silently,
    )
    msg = EmailMultiAlternatives(subject, html_content, from_email, to)
    msg.attach_alternative(html_content, "text/html")
    email_messages.append(msg)
    conn = mail.get_connection()
    conn.open()
    conn.send_messages(email_messages)
    conn.close()

    return None
