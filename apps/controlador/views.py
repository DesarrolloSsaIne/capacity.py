import smtplib

from django.core import mail
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.models import User, Group
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models.deletion import ProtectedError
from django.db.models import Q
from django.utils.module_loading import import_string
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from apps.controlador.models import Ges_Controlador
from apps.periodos.models import Glo_Periodos
from apps.controlador.forms import controladorFlujoForm, GestionControladorUpdateForm
from apps.jefaturas.models import Ges_Jefatura
from apps.estructura.models import Ges_Niveles, Ges_CuartoNivel, Ges_TercerNivel, Ges_SegundoNivel, Ges_PrimerNivel
from apps.estado_flujo.models import Glo_EstadoFlujo
from datetime import date
from django.db.models import Case, CharField, Value, When
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context

from django.conf import settings

from apps.registration.models import logEventos


class ControladorList(ListView):
    model = Ges_Controlador
    template_name = 'controlador/controlador_list.html'

    def get_context_data(self,  **kwargs):
        context = super(ControladorList, self).get_context_data(**kwargs)
        id_usuario_actual= self.request.user.id #obtiene id usuario actual

        try:
            periodo_actual = Glo_Periodos.objects.get(id_estado=1)
        except Glo_Periodos.DoesNotExist:
            return None

        lista_horas = Ges_Controlador.objects.filter(id_periodo=periodo_actual.id)
        context['object_list'] = lista_horas
        return context



class ControladorCreate(SuccessMessageMixin, CreateView):
    model = Ges_Controlador
    form_class = controladorFlujoForm
    template_name = 'controlador/controlador_form.html'

    def get_form_kwargs(self, **kwargs):
        kwargs = super(ControladorCreate, self).get_form_kwargs()
        try:
            periodo_actual = Glo_Periodos.objects.get(id_estado=1)
        except Glo_Periodos.DoesNotExist:
            return None
        kwargs['id_periodo'] = periodo_actual
        return kwargs

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        jefatura = request.POST['id_jefatura']
        nivel_jefatura= Ges_Jefatura.objects.get(id=jefatura)
        nivel_inicial = Ges_Niveles.objects.get(id=nivel_jefatura.id_nivel_id)

        user_id_jefatura=nivel_jefatura.id_user

        periodo= Glo_Periodos.objects.get(id_estado=1)
        estado_flujo = Glo_EstadoFlujo.objects.get(estado=2)

        if form.is_valid():
            form.instance.nivel_inicial=nivel_inicial.orden_nivel
            form.instance.id_periodo = periodo
            form.instance.estado_flujo= estado_flujo
            form.instance.fecha_ultima_modificacion= date.today()



            form.save()

            g = Group.objects.get(id=1)
            g.user_set.add(user_id_jefatura)

            request.session['message_class'] = "alert alert-success"
            messages.success(self.request, "Los datos fueron creados correctamente!")
            return HttpResponseRedirect('/controlador/listar')
        else:
            request.session['message_class'] = "alert alert-danger"
            messages.error(self.request, "Error interno: No se ha creado el registro. Comuníquese con el administrador.")
            return HttpResponseRedirect('/controlador/listar')


class ControladorDelete(SuccessMessageMixin, DeleteView ):
    model = Ges_Controlador
    template_name = 'controlador/controlador_delete.html'

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        try:

            id_controlador = self.kwargs['pk']
            nivel_jefatura = Ges_Controlador.objects.get(id=id_controlador)
            user_id_jefatura = nivel_jefatura.id_jefatura.id_user

            obj.delete()

            g = Group.objects.get(id=1)
            g.user_set.remove(user_id_jefatura)


            request.session['message_class'] = "alert alert-success"
            messages.success(self.request, "El registro fue eliminado correctamente!")
            return HttpResponseRedirect('/controlador/listar')

        except ProtectedError as e:
            request.session['message_class'] = "alert alert-danger"
            messages.error(request, "Error de integridad: .")
            return HttpResponseRedirect('/controlador/listar')

        except Exception  as e:
            request.session['message_class'] = "alert alert-danger"
            messages.error(request, "Error interno: No se ha eliminado el registro. Comuníquese con el administrador.")
            return HttpResponseRedirect('/controlador/listar')




########################################################################################################################
########################################################################################################################
########################################################################################################################








class ControladorUpdate(UpdateView):
    model = Ges_Controlador
    form_class = GestionControladorUpdateForm
    template_name = 'controlador/actividades_enviar.html'

    def get_form_kwargs(self, **kwargs):
        kwargs = super(ControladorUpdate, self).get_form_kwargs()
        id_usuario_actual = self.request.user.id
        try:
            periodo_actual = Glo_Periodos.objects.get(id_estado=1)
        except Glo_Periodos.DoesNotExist:
            return None
        try:
            nivel_usuario = Ges_Jefatura.objects.get(Q(id_user=id_usuario_actual) & Q(id_periodo=periodo_actual.id))

        except Ges_Jefatura.DoesNotExist:
            return None

        id_nivel = nivel_usuario.id_nivel.id
        replies = Ges_Niveles.objects.filter(Q(id=id_nivel) & Q(id_periodo=periodo_actual.id)).annotate(
            nivel_order=Case(
                When(orden_nivel=1, then='id_primer_nivel'),
                When(orden_nivel=2, then='id_segundo_nivel'),
                When(orden_nivel=3, then='id_tercer_nivel'),
                When(orden_nivel=4, then='id_cuarto_nivel'),
                output_field=CharField(),
            )
        )
        for nivel in replies:
            id_nivel_final = nivel.nivel_order
            id_orden = nivel.orden_nivel


        if id_orden == 2:
            id_primerNivel = Ges_SegundoNivel.objects.get(id=id_nivel_final)
        if id_orden == 3:
            id_SegundoNivel = Ges_TercerNivel.objects.get(id=id_nivel_final)
        if id_orden == 4:
            id_tercerNivel = Ges_CuartoNivel.objects.get(id=id_nivel_final)

        if id_orden == 2:
            id_nivel_jefsuperior = Ges_Niveles.objects.get(id_primer_nivel=id_primerNivel.primer_nivel_id)
        if id_orden == 3:
            id_nivel_jefsuperior = Ges_Niveles.objects.get(id_segundo_nivel=id_SegundoNivel.segundo_nivel_id)
        if id_orden == 4:
            id_nivel_jefsuperior = Ges_Niveles.objects.get(id_tercer_nivel=id_tercerNivel.tercer_nivel_id)

        id_jef_final = Ges_Jefatura.objects.get(id_nivel=id_nivel_jefsuperior.id) # SI NO ENCUENTRA UN JEFE SE CAE, VALIDAR
        id_jef_final = int(id_jef_final.id_nivel_id)
        kwargs['nivel_jefatura'] = id_jef_final
        return kwargs

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        id_nivel = kwargs['pk']
        id_nivel = int(id_nivel)
        instancia_nivel = self.model.objects.get(id=id_nivel)
        id_jefatura = request.POST['jefatura_primerarevision']
        id_jefatura_solicita = request.POST['id_jefatura']
        id_usuario_actual = self.request.user.id
        id_nivel_post = Ges_Jefatura.objects.get(id=id_jefatura)
        id_nivel_post = id_nivel_post.id_nivel_id
        form = self.form_class(id_nivel_post, request.POST, instance=instancia_nivel)

        try:
            periodo_actual = Glo_Periodos.objects.get(id_estado=1)
        except Glo_Periodos.DoesNotExist:
            return None
        idcorreoJefaturaOb =   Ges_Jefatura.objects.get(id=id_jefatura)
        idcorreoJefatura=  idcorreoJefaturaOb
        idcorreoJefatura = idcorreoJefatura.id_user_id
        idcorreoJefatura = User.objects.get(id=idcorreoJefatura)
        nivel_usuario = Ges_Jefatura.objects.get(Q(id_user=id_usuario_actual) & Q(id_periodo=periodo_actual.id))
        idcorreoJefatura = [idcorreoJefatura.email]
        subject = 'Revisión Plan ' + str(nivel_usuario.id_nivel.descripcion_nivel)
        message= 'Estimada(o) Usuaria(o), Se ha asignado a usted una tarea de revisión de plan de trabajo.  Atte. Subdpto. de Planificación Institucional.>Correo generado automaticamente no responder.'
        messageHtml = 'Estimada(o) Usuaria(o),<br> Se ha asignado a usted una tarea de revisión plan de trabajo<br> Atte. <br>Subdpto. de Planificación Institucional.<br><p style="font-size:12px;color:red;">correo generado automaticamente favor no responder.'



        if form.is_valid():
            form.save()
            #send_correo(idcorreoJefatura, subject, message, messageHtml)
            #send_correo(idcorreoJefatura, subject, message, messageHtml)

            update_state(id_jefatura_solicita,id_jefatura,  4)
            tipo_evento = "Envío Plan a primera revisión"
            metodo = "Controlador - ControladorUpdate"
            usuario_evento = nivel_usuario.id_user
            jefatura_dirigida = idcorreoJefaturaOb.id_user
            logEventosCreate(tipo_evento, metodo, usuario_evento, jefatura_dirigida)
            request.session['message_class'] = "alert alert-success"
            messages.success(self.request, "El plan fue enviado para su revisión.")
            return HttpResponseRedirect('/actividades/listar')
        else:
            request.session['message_class'] = "alert alert-danger"
            messages.error(self.request, "Error interno: No se ha actualizado el registro. Comuníquese con el administrador.")
            return HttpResponseRedirect('/actividades/listar')

#def send_correo(email, subject, message, messageHtml):

       #email = email
       #subject = subject
        #       from_email = settings.EMAIL_HOST_USER
      # send_mail(subject, message, from_email , [email],fail_silently=False)

       #subject, from_email, to = subject, from_email, email
       #text_content = message
       #html_content = messageHtml
       #msg = EmailMultiAlternatives(subject, text_content, from_email, to)
       #msg.attach_alternative(html_content, "text/html")
       #msg.send()


       #return None


#def send_correo():
    #    From = 'benjamin.vasquez@ine.cl'
    #Recipient = 'benjamin.vasquez@ine.cl'

    #Messege = 'Hola'

    # Credentials
    #username = 'bvasquez'
    #password = '(ine2022)'

    # mail is being sent :
    #server = smtplib.SMTP('192.168.1.235:25')
    #server.starttls()
    #server.login(username, password)
    #server.sendmail(From, Recipient, Messege)
    #server.quit()

    #return None


def get_connection(backend=None, fail_silently=False, **kwds):
    klass = import_string(backend or settings.EMAIL_BACKEND)
    return klass(fail_silently=fail_silently, **kwds)

def send_correo(email, subject, message, messageHtml):
    # email = email
    # subject = subject
    from_email = settings.EMAIL_HOST_USER
    # send_mail(subject, message, from_email , [email],fail_silently=False)
    email_messages = []
    subject, from_email, to = subject, from_email, email
    text_content = message
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
    msg = EmailMultiAlternatives(subject, text_content, from_email, to)
    msg.attach_alternative(html_content, "text/html")
    email_messages.append(msg)
    conn = mail.get_connection()
    conn.open()
    conn.send_messages(email_messages)
    conn.close()
    #msg.send()

    return None

def checkmailserver():
    from django.core.mail import get_connection
    errors = []
    connection = get_connection(username=None,
       password=None,
       fail_silently=False)
    try:
        connection.open()
    except Exception:
       errors='error'
    else:
        connection.close()


    return errors


def update_state(id_jefatura,id_revisa, estado):
    try:
        periodo_actual = Glo_Periodos.objects.get(id_estado=1)
    except Glo_Periodos.DoesNotExist:
        return None
    controlador = Ges_Controlador.objects.get(Q(id_jefatura=id_jefatura)& Q(id_periodo=periodo_actual.id)& Q(jefatura_primerarevision=id_revisa))
    estado = estado
    controlador.estado_flujo_id = int(estado)
    controlador.save()
    return None



def logEventosCreate(tipo_evento, metodo ,usuario_evento, jefatura_dirigida):
    logEventos.objects.create(
        tipo_evento=tipo_evento,
        metodo=metodo,
        usuario_evento=usuario_evento,
        jefatura_dirigida=jefatura_dirigida,
    )
    return None