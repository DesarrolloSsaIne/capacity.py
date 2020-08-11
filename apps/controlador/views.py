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
from apps.actividades.models import Ges_Actividad
from apps.controlador.models import Ges_Controlador
from apps.periodos.models import Glo_Periodos
from apps.controlador.forms import controladorFlujoForm, GestionControladorUpdateForm
from apps.jefaturas.models import Ges_Jefatura
from apps.estructura.models import Ges_Niveles, Ges_CuartoNivel, Ges_TercerNivel, Ges_SegundoNivel, Ges_PrimerNivel
from apps.estado_flujo.models import Glo_EstadoFlujo
from datetime import date
from django.db.models import Case, CharField, Value, When
from django.contrib import messages
from django.core.mail import EmailMessage,send_mass_mail
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

        try:
            id_jef_final = Ges_Jefatura.objects.get(
                id_nivel=id_nivel_jefsuperior.id)  # SI NO ENCUENTRA UN JEFE SE CAE, VALIDAR
        except Ges_Jefatura.DoesNotExist:
            id_jef_final = 0
            pass

        if id_jef_final != 0:
            id_jef_final = int(id_jef_final.id_nivel_id)
            kwargs['nivel_jefatura'] = id_jef_final
            return kwargs
        else:

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

        nivel_usuario = Ges_Jefatura.objects.get(Q(id_user=id_usuario_actual) & Q(id_periodo=periodo_actual.id))
        idcorreoJefaturaOb =   Ges_Jefatura.objects.get(id=id_jefatura)
        Actividades = Ges_Actividad.objects.filter(Q(id_periodo=periodo_actual.id) & Q(
            id_controlador=instancia_nivel.id)).count()

        if Actividades != 0:

            if form.is_valid():
                form.save()

                update_state(id_jefatura_solicita,id_jefatura,  4)
                tipo_evento = "Envío Plan a primera revisión"
                metodo = "Controlador - ControladorUpdate"
                usuario_evento = nivel_usuario.id_user
                jefatura_dirigida = idcorreoJefaturaOb.id_user
                logEventosCreate(tipo_evento, metodo, usuario_evento, jefatura_dirigida)

                try:

                    EnviarCorreoCierre(id_jefatura, nivel_usuario.id_nivel.descripcion_nivel)
                    request.session['message_class'] = "alert alert-success"  # Tipo mensaje
                    messages.success(request,
                                     "El plan fue enviado para su revisión y el correo de notificación fue enviado a su jefatura directa.!")  # mensaje
                    return HttpResponseRedirect('/actividades/listar')  # Redirije a la pantalla principal

                except:

                    request.session['message_class'] = "alert alert-warning"  # Tipo mensaje
                    messages.success(request,
                                     "El plan fue enviado para su revisión! , pero el servicio de correo tuvo un inconveniente favor comuníquese con su jefatura directa para informarle el envío del plan para revisión.")  # mensaje
                    return HttpResponseRedirect('/actividades/listar')  # Redirije a la pantalla principal

            else:

                request.session['message_class'] = "alert alert-danger"
                messages.error(self.request,
                               "Error interno: No se ha enviado el plan para revisión. Comuníquese con el administrador.")
                return HttpResponseRedirect('/actividades/listar')








def EnviarCorreoCierre(id_jefatura, descripcion_nivel):
    try:
        periodo_actual = Glo_Periodos.objects.get(id_estado=1)
    except Glo_Periodos.DoesNotExist:
        return None

    controladorPlan = Ges_Jefatura.objects.values_list('id_user__email' , flat=True).filter(Q(id_periodo=periodo_actual) & Q(id=id_jefatura))
    idcorreoJefatura=list(controladorPlan)

    subject = 'Revisión Plan ' + str(descripcion_nivel)
    messageHtml = 'Estimada(o) Usuaria(o),<br> Se informa que se le ha asignado un plan de gestión para su revisión, ingrese al sitio de capacity institucional y revise su banjeda.<br> Atte. <br>Subdpto. de Planificación Institucional.<br><p style="font-size:12px;color:red;">correo generado automaticamente favor no responder.'

    email = EmailMessage(subject, messageHtml ,to=idcorreoJefatura)

    email.content_subtype='html'
    email.send()





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