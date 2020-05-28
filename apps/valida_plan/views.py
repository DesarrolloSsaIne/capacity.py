from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from apps.estructura.models import Ges_Niveles
from apps.jefaturas.models import Ges_Jefatura
from apps.controlador.models import Ges_Controlador
from django.db.models import Q
from apps.periodos.models import Glo_Periodos
from apps.actividades.models import Ges_Actividad
from apps.objetivos.models import  Ges_Objetivo_Operativo, Ges_Objetivo_Tactico, Ges_Objetivo_TacticoTN
from apps.valida_plan.forms import ValidaPlanObservacionesForm,ObservacionForm, RechazaPlanUpdateForm, ValidaPlanUpdateForm
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from apps.valida_plan.models import Ges_Observaciones
from apps.valida_plan2.models import Ges_Observaciones_sr
from django.db.models import Subquery, OuterRef, Count # import agregados por JR - sprint 8 - ok
from django.db.models.deletion import ProtectedError
from apps.periodos.models import Glo_Seguimiento

from django.core import mail
from django.conf import settings
from django.utils.module_loading import import_string
from django.core.mail import EmailMultiAlternatives
from django.db.models.deletion import ProtectedError
from django.http import JsonResponse
#Nuevo JP
from apps.controlador.forms import controladorFlujoForm, GestionControladorUpdateForm
from django.db.models import Case, CharField, Value, When
from apps.estructura.models import Ges_Niveles, Ges_CuartoNivel, Ges_TercerNivel, Ges_SegundoNivel, Ges_PrimerNivel
from django.contrib.auth.models import User
from apps.registration.models import logEventos
from datetime import datetime

from apps.eje.models import Ges_Ejes

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
    # msg.send()

    return None



class RechazaPlan(UpdateView):
    model = Ges_Controlador
    form_class = RechazaPlanUpdateForm
    template_name = 'valida_plan/valida_plan_rechaza_form.html'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        id_controlador = kwargs['pk']
        id_usuario_actual = self.request.user.id  # obtiene id usuario actual

        try:
            periodo_actual = Glo_Periodos.objects.get(id_estado=1)
        except Glo_Periodos.DoesNotExist:
            return None

        controla = self.model.objects.get(id=id_controlador)
        email_jefatura = controla.id_jefatura.id_user.email    #correo de rechazo

        lista_actividades = Ges_Actividad.objects.filter(Q(id_controlador=id_controlador) & Q(id_periodo=periodo_actual.id))
        totalObservacion = 0


        for actvidades in list(lista_actividades):
            valor = actvidades
            ExisteObservacion = Ges_Observaciones.objects.filter(Q(id_periodo=periodo_actual.id) & Q(id_actividad=valor)).count()
            if ExisteObservacion > 0:
                totalObservacion = totalObservacion + 1
        lista_actividades

        instancia_nivel = self.model.objects.get(id=id_controlador)
        form = self.form_class(request.POST, instance=instancia_nivel)

        if totalObservacion > 0:
            if form.is_valid():
                form.save()
                idcorreoJefatura = [email_jefatura]
                subject = 'Rechazo de Plan'
                message = 'Estimada(o) Usuaria(o), Se ha realizado un rechazo al plan que ha ingresado.  Atte. Subdpto. de Planificación Institucional.>Correo generado automaticamente no responder.'
                messageHtml = 'Estimada(o) Usuaria(o),<br> El plan que ha Ud ha enviado ha sido rechazado. <br> Atte. <br>Subdpto. de Planificación Institucional.<br><p style="font-size:12px;color:red;">correo generado automaticamente favor no responder.'
                #send_correo(idcorreoJefatura, subject, message, messageHtml)

                request.session['message_class'] = "alert alert-success"
                messages.success(self.request, "El Plan fue rechazado correctamente y enviado al usuario que lo formuló.")
                return HttpResponseRedirect('/valida_plan/listarUnidades')
            else:
                request.session['message_class'] = "alert alert-danger"
                messages.error(self.request, "Error interno: El plan no ha podido ser rechazado. Comuníquese con el administrador.")
                return HttpResponseRedirect('/valida_plan/listarUnidades')
        else:
            request.session['message_class'] = "alert alert-danger"
            messages.error(self.request, "Debe ingresar al menos una observacion para rechazar el plan.")
            return HttpResponseRedirect('/valida_plan/listarUnidades')


class AceptaPlan(UpdateView):
    model = Ges_Controlador
    form_class = ValidaPlanUpdateForm
    template_name = 'valida_plan/valida_plan_acepta_form.html'

    def get_form_kwargs(self, **kwargs):
        kwargs = super(AceptaPlan, self).get_form_kwargs()
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

        if id_orden == 1:
            id_direccion = Ges_PrimerNivel.objects.get(id=id_nivel_final)
        if id_orden == 2:
            id_primerNivel = Ges_SegundoNivel.objects.get(id=id_nivel_final)
        if id_orden == 3:
            id_SegundoNivel = Ges_TercerNivel.objects.get(id=id_nivel_final)
        if id_orden == 4:
            id_tercerNivel = Ges_CuartoNivel.objects.get(id=id_nivel_final)

        if id_orden == 1:
            id_nivel_jefsuperior = Ges_Niveles.objects.get(id_primer_nivel=id_direccion.id)
        if id_orden == 2:
            id_nivel_jefsuperior = Ges_Niveles.objects.get(id_primer_nivel=id_primerNivel.primer_nivel_id)
        if id_orden == 3:
            id_nivel_jefsuperior = Ges_Niveles.objects.get(id_segundo_nivel=id_SegundoNivel.segundo_nivel_id)
        if id_orden == 4:
            id_nivel_jefsuperior = Ges_Niveles.objects.get(id_tercer_nivel=id_tercerNivel.tercer_nivel_id)
        try:

            id_jef_final = Ges_Jefatura.objects.get(id_nivel=id_nivel_jefsuperior.id)
            id_jef_final = int(id_jef_final.id_nivel_id)
        except Ges_Jefatura.DoesNotExist:
                pass

        kwargs['nivel_jefatura'] = id_jef_final
        return kwargs

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        id_nivel = kwargs['pk']
        id_nivel = int(id_nivel)
        instancia_nivel = self.model.objects.get(id=id_nivel)
        id_jefatura = request.POST['jefatura_segundarevision']
        id_jefatura_solicita = request.POST['id_jefatura']
        id_usuario_actual = self.request.user.id

        try:
            periodo_actual = Glo_Periodos.objects.get(id_estado=1)
        except Glo_Periodos.DoesNotExist:
            return None

        if int(id_jefatura) != 0:

            id_nivel_post = Ges_Jefatura.objects.get(id=id_jefatura)
            id_nivel_post = id_nivel_post.id_nivel_id

            form = self.form_class(id_nivel_post, request.POST, instance=instancia_nivel)

            idcorreoJefaturaOb = Ges_Jefatura.objects.get(id=id_jefatura)
            idcorreoJefatura = idcorreoJefaturaOb
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

                d_jefatura = Ges_Jefatura.objects.get(id_user=id_usuario_actual)
                update_state(id_jefatura_solicita, id_jefatura, 5, d_jefatura.id)

                tipo_evento = "Envío Plan a segunda revisión."
                metodo = "Controlador - AceptaPlan"
                usuario_evento = nivel_usuario.id_user
                jefatura_dirigida = idcorreoJefaturaOb.id_user
                logEventosCreate(tipo_evento, metodo, usuario_evento, jefatura_dirigida)

                request.session['message_class'] = "alert alert-success"
                messages.success(self.request, "El plan fue enviado para su revisión.")
                return HttpResponseRedirect('/valida_plan/listarUnidades')
            else:
                request.session['message_class'] = "alert alert-danger"
                messages.error(self.request, "Error interno: No se ha actualizado el registro. Comuníquese con el administrador.")
                return HttpResponseRedirect('/valida_plan/listarUnidades')
        else:
            d_jefatura = Ges_Jefatura.objects.get(id_user=id_usuario_actual)
            controlador = Ges_Controlador.objects.get(Q(id= id_nivel) & Q(id_periodo=periodo_actual.id))
            existeAnalista = controlador.analista_asignado
            estado = 0
            if existeAnalista:
                estado = 6
            else:
                estado = 10
            estado = int(estado)
            update_state(id_jefatura_solicita, '', estado, d_jefatura.id)
            nivel_usuario = Ges_Jefatura.objects.get(Q(id_user=id_usuario_actual) & Q(id_periodo=periodo_actual.id))

            tipo_evento = "Envío Plan a planifificaión"
            metodo = "Controlador - AceptaPlan"
            usuario_evento = nivel_usuario.id_user
            jefatura_dirigida = nivel_usuario.id_user
            logEventosCreate(tipo_evento, metodo, usuario_evento, jefatura_dirigida)

            request.session['message_class'] = "alert alert-success"
            messages.success(self.request, "El plan fue enviado para su revisión.")
            return HttpResponseRedirect('/valida_plan/listarUnidades')


def update_state(id_jefatura,id_revisa, estado, id_primerrevisor):
    try:
        periodo_actual = Glo_Periodos.objects.get(id_estado=1)
    except Glo_Periodos.DoesNotExist:
        return None
    controlador = Ges_Controlador.objects.get(Q(id_jefatura=id_jefatura) & Q(id_periodo=periodo_actual.id) & Q(jefatura_primerarevision=id_primerrevisor))
    estado = estado
    controlador.estado_flujo_id = int(estado)
    controlador.jefatura_segundarevision_id = id_revisa
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


def Updatejefatura_segundarevision(id_cont, id_segundoRevisor): #Función creada por JR - sprint 8- OK
    Ges_Controlador.objects.filter(id=id_cont).update(
        jefatura_segundarevision=id_segundoRevisor,
    )
    pass
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################

class UnidadesList(ListView): #Modificado por JR- sprint 8 - OK
    model = Ges_Niveles
    template_name = 'valida_plan/valida_plan_list.html'

    def get_context_data(self, **kwargs):
        context = super(UnidadesList, self).get_context_data(**kwargs)
        id_usuario_actual = self.request.user.id  # obtiene id usuario actual

        try:
            periodo_actual = Glo_Periodos.objects.get(id_estado=1)
        except Glo_Periodos.DoesNotExist:
            return None

        try:
            id_jefatura = Ges_Jefatura.objects.get(id_user=id_usuario_actual)

            count_no_vistos = Ges_Observaciones.objects.values('id_controlador').filter(
                id_controlador=OuterRef('pk')).annotate(
                count_id_actividad=Count('id', filter=Q(observado=1)  & Q(id_periodo=periodo_actual.id) & (~Q(user_observa=id_usuario_actual))))

            count_observaciones = Ges_Observaciones.objects.values('id_controlador').filter(
                id_controlador=OuterRef('pk')).annotate(
                count_id_actividad=Count('id'))


            id_controlador = Ges_Controlador.objects.filter(
                Q(jefatura_primerarevision=id_jefatura.id) & Q(id_periodo=periodo_actual.id) & Q(estado_flujo=4)).annotate(
                count_no_vistos=Subquery(count_no_vistos.values('count_id_actividad')),
                count_observaciones=Subquery(count_observaciones.values('count_id_actividad')[0:1])).order_by(
                '-count_no_vistos', '-count_observaciones')

            id_jefatura = Ges_Jefatura.objects.filter(id_user=id_usuario_actual)

            context['object_list'] = id_controlador
           # context['object_list3'] = id_jefatura

            return context

        except Ges_Jefatura.DoesNotExist:
            context['habilitado'] = {'mensaje': False}
            return None


class Objetivos(ListView): #Modificado por JR- sprint 8 - OK
    model = Ges_Actividad
    template_name = 'valida_plan/valida_plan_detalle.html'

    def get_context_data(self, **kwargs):
        context = super(Objetivos, self).get_context_data(**kwargs)
        id_usuario_actual = self.request.user.id  # obtiene id usuario actual
        self.request.session['id_nivel_controlador']=self.kwargs['pk'] #guarda id  controlador

        try:
            periodo_actual = Glo_Periodos.objects.get(id_estado=1)
        except Glo_Periodos.DoesNotExist:
            return None

        try:
            controlador = Ges_Controlador.objects.get(Q(id=self.kwargs['pk']) & Q(id_periodo=periodo_actual.id))
        except Ges_Controlador.DoesNotExist:
            return None

        id_orden = controlador.nivel_inicial
        self.request.session['id_controlador_real'] = controlador.id
       # vaar= controlador.id_jefatura.id_nivel_id

        id_nivel = Ges_Niveles.objects.get(
            Q(id=controlador.id_jefatura.id_nivel_id) & Q(id_periodo=periodo_actual.id))


        try:
           # id_jefatura = Ges_Jefatura.objects.get(id_user=id_usuario_actual)
           # id_controlador = Ges_Controlador.objects.get(Q(jefatura_primerarevision=id_jefatura.id) & Q(id_periodo=periodo_actual.id) & Q(id=controlador.id)) #que pasa cuando hay más de una jefatura?




            if id_orden == 3:
               # replies2 = Ges_Objetivo_TacticoTN.objects.filter(id_tercer_nivel_id=id_nivel.id_tercer_nivel_id)
                count_no_vistos = Ges_Observaciones.objects.values('id_objetivo').filter(
                    id_objetivo=OuterRef('pk')).annotate(
                    count_id_actividad=Count('id', filter=Q(observado=1)  & Q(id_periodo=periodo_actual.id) & (~Q(user_observa=id_usuario_actual))))

                count_observaciones = Ges_Observaciones.objects.values('id_objetivo').filter(
                    id_objetivo=OuterRef('pk')).annotate(
                    count_id_actividad=Count('id'))

                count_actividades = Ges_Actividad.objects.values('id_objetivo_tacticotn').filter(
                    id_objetivo_tacticotn=OuterRef('pk')).annotate(
                    count_id_actividad=Count('id', filter=Q(id_periodo=periodo_actual.id)))

                count_no_vistos_obj = Ges_Observaciones_sr.objects.values('id_objetivo_tacticotn').filter(
                    id_objetivo_tacticotn=OuterRef('pk')).annotate(
                    count_id_actividad=Count('id', filter=Q(observado=1) & Q(id_periodo=periodo_actual.id) & (
                        ~Q(user_observa=id_usuario_actual))))

                replies2 = Ges_Objetivo_TacticoTN.objects.filter(
                    Q(id_tercer_nivel_id=id_nivel.id_tercer_nivel_id) & Q(id_periodo=periodo_actual.id)).annotate(
                    count_no_vistos=Subquery(count_no_vistos.values('count_id_actividad')),
                    count_actividades=Subquery(count_actividades.values('count_id_actividad')),
                    count_no_vistos_obj=Subquery(count_no_vistos_obj.values('count_id_actividad')),
                    count_observaciones=Subquery(count_observaciones.values('count_id_actividad'))).order_by(
                    '-count_no_vistos', '-count_observaciones')


            if id_orden == 2:
               # replies2 = Ges_Objetivo_Tactico.objects.filter(id_segundo_nivel_id=id_nivel.id_segundo_nivel_id)
                count_no_vistos = Ges_Observaciones.objects.values('id_objetivo').filter(
                    id_objetivo=OuterRef('pk')).annotate(
                    count_id_actividad=Count('id', filter=Q(observado=1)  & Q(id_periodo=periodo_actual.id) & (~Q(user_observa=id_usuario_actual))))

                count_observaciones = Ges_Observaciones.objects.values('id_objetivo').filter(
                    id_objetivo=OuterRef('pk')).annotate(
                    count_id_actividad=Count('id'))

                count_actividades = Ges_Actividad.objects.values('id_objetivo_tactico').filter(
                    id_objetivo_tactico=OuterRef('pk')).annotate(
                    count_id_actividad=Count('id', filter=Q(id_periodo=periodo_actual.id)))

                count_no_vistos_obj = Ges_Observaciones_sr.objects.values('id_objetivo_tactico').filter(
                    id_objetivo_tactico=OuterRef('pk')).annotate(
                    count_id_actividad=Count('id', filter=Q(observado=1) & Q(id_periodo=periodo_actual.id) & (
                       ~Q(user_observa=id_usuario_actual))))

                replies2 = Ges_Objetivo_Tactico.objects.filter(
                    Q(id_segundo_nivel_id=id_nivel.id_segundo_nivel_id) & Q(id_periodo=periodo_actual.id)).annotate(
                    count_no_vistos=Subquery(count_no_vistos.values('count_id_actividad')),
                    count_actividades=Subquery(count_actividades.values('count_id_actividad')),
                    count_no_vistos_obj=Subquery(count_no_vistos_obj.values('count_id_actividad')),
                    count_observaciones=Subquery(count_observaciones.values('count_id_actividad'))).order_by(
                    '-count_no_vistos', '-count_observaciones')


            if id_orden == 4:
               # replies2 = Ges_Objetivo_Operativo.objects.filter(id_cuarto_nivel_id=id_nivel.id_cuarto_nivel_id)

                count_no_vistos = Ges_Observaciones.objects.values('id_objetivo').filter(
                    id_objetivo=OuterRef('pk')).annotate(
                    count_id_actividad=Count('id', filter=Q(observado=1)  & Q(id_periodo=periodo_actual.id) & (~Q(user_observa=id_usuario_actual))))

                count_observaciones = Ges_Observaciones.objects.values('id_objetivo').filter(
                    id_objetivo=OuterRef('pk')).annotate(
                    count_id_actividad=Count('id'))

                count_actividades = Ges_Actividad.objects.values('id_objetivo_operativo').filter(
                    id_objetivo_operativo=OuterRef('pk')).annotate(
                    count_id_actividad=Count('id', filter=Q(id_periodo=periodo_actual.id)))

                count_no_vistos_obj = Ges_Observaciones_sr.objects.values('id_objetivo_operativo').filter(
                    id_objetivo_operativo=OuterRef('pk')).annotate(
                    count_id_actividad=Count('id', filter=Q(observado=1) & Q(id_periodo=periodo_actual.id) & (
                        ~Q(user_observa=id_usuario_actual))))

                replies2 = Ges_Objetivo_Operativo.objects.filter(
                    Q(id_cuarto_nivel_id=id_nivel.id_cuarto_nivel_id) & Q(id_periodo=periodo_actual.id)).annotate(
                    count_no_vistos=Subquery(count_no_vistos.values('count_id_actividad')),
                    count_actividades=Subquery(count_actividades.values('count_id_actividad')),
                    count_no_vistos_obj=Subquery(count_no_vistos_obj.values('count_id_actividad')),
                    count_observaciones=Subquery(count_observaciones.values('count_id_actividad'))).order_by(
                    '-count_no_vistos', '-count_observaciones')



            context['orden'] = {'orden_nivel': id_orden}
            context['niveles'] = replies2
            context['objetivo'] = id_nivel

            self.request.session['id_orden'] = id_orden


            return context

        except Ges_Jefatura.DoesNotExist:
            context['habilitado'] = {'mensaje': False}


            return None

class Actividades(ListView): # Modificado por JR- sprint 8 - OK
    model = Ges_Actividad
    template_name = 'valida_plan/valida_plan_list_actividades.html'

    def get_context_data(self,  **kwargs):
        context = super(Actividades, self).get_context_data(**kwargs)
        id_usuario_actual = self.request.user.id  # obtiene id usuario actual

        try:
            periodo_actual = Glo_Periodos.objects.get(id_estado=1)
        except Glo_Periodos.DoesNotExist:
            return None

        self.request.session['id_objetivo']=self.kwargs['pk']#315

        nombre = ""
        if self.request.session['id_orden']==2:
           # lista_actividades = Ges_Actividad.objects.filter(Q(id_objetivo_tactico=self.kwargs['pk']) & Q(id_periodo=periodo_actual.id))

            count_no_vistos = Ges_Observaciones.objects.values('id_actividad_id').filter(id_actividad=OuterRef('pk')).annotate(
              count_id_actividad=Count('id', filter=Q(observado=1) & Q(id_periodo=periodo_actual.id) & (~Q(user_observa=id_usuario_actual))))

            count_observaciones = Ges_Observaciones.objects.values('id_actividad_id').filter(id_actividad=OuterRef('pk')).annotate(
            count_id_actividad=Count('id'))

            lista_actividades = Ges_Actividad.objects.filter(
              Q(id_objetivo_tactico=self.kwargs['pk']) & Q(id_periodo=periodo_actual.id)).annotate(
              count_no_vistos=Subquery(count_no_vistos.values('count_id_actividad')),

                count_observaciones=Subquery(count_observaciones.values('count_id_actividad'))).order_by('-count_no_vistos','-fecha_registro')

            nombre=  Ges_Objetivo_Tactico.objects.get(id=self.kwargs['pk'])

        if self.request.session['id_orden']==3:
           # lista_actividades = Ges_Actividad.objects.filter(Q(id_objetivo_tacticotn=self.kwargs['pk']) & Q(id_periodo=periodo_actual.id))

            count_no_vistos = Ges_Observaciones.objects.values('id_actividad_id').filter(id_actividad=OuterRef('pk')).annotate(
              count_id_actividad=Count('id', filter=Q(observado=1) & Q(id_periodo=periodo_actual.id) & (~Q(user_observa=id_usuario_actual))))
            count_observaciones = Ges_Observaciones.objects.values('id_actividad_id').filter(id_actividad=OuterRef('pk')).annotate(
            count_id_actividad=Count('id'))


            lista_actividades = Ges_Actividad.objects.filter(
              Q(id_objetivo_tacticotn=self.kwargs['pk']) & Q(id_periodo=periodo_actual.id)).annotate(
              count_no_vistos=Subquery(count_no_vistos.values('count_id_actividad')),


                count_observaciones=Subquery(count_observaciones.values('count_id_actividad'))).order_by('-count_no_vistos','-fecha_registro')


            nombre = Ges_Objetivo_TacticoTN.objects.get(id=self.kwargs['pk'])

        if self.request.session['id_orden']==4:

            count_no_vistos = Ges_Observaciones.objects.values('id_actividad_id').filter(id_actividad=OuterRef('pk')).annotate(
              count_id_actividad=Count('id', filter=Q(observado=1) & Q(id_periodo=periodo_actual.id) & (~Q(user_observa=id_usuario_actual))))
            count_observaciones = Ges_Observaciones.objects.values('id_actividad_id').filter(id_actividad=OuterRef('pk')).annotate(
            count_id_actividad=Count('id'))

            lista_actividades = Ges_Actividad.objects.filter(
              Q(id_objetivo_operativo=self.kwargs['pk']) & Q(id_periodo=periodo_actual.id)).annotate(
              count_no_vistos=Subquery(count_no_vistos.values('count_id_actividad')),

                count_observaciones=Subquery(count_observaciones.values('count_id_actividad'))).order_by('-count_no_vistos','-fecha_registro')


            nombre = Ges_Objetivo_Operativo.objects.get(id=self.kwargs['pk'])

        try:
            nivel_usuario = Ges_Jefatura.objects.get(Q(id_user=id_usuario_actual) & Q(id_periodo=periodo_actual.id))
        except Ges_Jefatura.DoesNotExist:
            context['habilitado'] = {'mensaje': False}
            return None


        context['object_list'] = lista_actividades
        context['nombre_objetivo'] = {'nombre': nombre}
        context['id_orden'] = {'id_orden': self.request.session['id_orden']}
        context['id_nivel_controlador']={'id': self.request.session['id_nivel_controlador']}

        #context['objetivo'] = id_nivel


        return context



#############################################################################################################
#############################################################################################################
#############################################################################################################

class SeguimientoUnidadesList(ListView): #Modificado por JR- sprint 10
    model = Ges_Niveles
    template_name = 'valida_plan/seguimiento_plan_list.html'

    def get_context_data(self, **kwargs):
        context = super(SeguimientoUnidadesList, self).get_context_data(**kwargs)
        id_usuario_actual = self.request.user.id  # obtiene id usuario actual

        try:
            periodo_actual = Glo_Periodos.objects.get(id_estado=1)
        except Glo_Periodos.DoesNotExist:
            return None

        id_jefatura = Ges_Jefatura.objects.get(id_user=id_usuario_actual)

        id_controlador = Ges_Controlador.objects.filter(
            Q(jefatura_primerarevision=id_jefatura.id) & Q(id_periodo=periodo_actual.id))

        try:
             estado= Glo_Seguimiento.objects.get(Q(id_estado_seguimiento=1) & Q(id_periodo=PeriodoActual()))
        except Glo_Seguimiento.DoesNotExist:
             estado = 0

        context['estado_seguimiento'] = estado
        context['object_list'] = id_controlador

        return context


class SeguimientoObjetivos(ListView): #Modificado por JR- sprint 8 - OK
    model = Ges_Actividad
    template_name = 'valida_plan/seguimiento_plan_detalle.html'

    def get_context_data(self, **kwargs):
        context = super(SeguimientoObjetivos, self).get_context_data(**kwargs)
        id_usuario_actual = self.request.user.id  # obtiene id usuario actual
        self.request.session['id_nivel_controlador']=self.kwargs['pk'] #guarda id  controlador

        try:
            periodo_actual = Glo_Periodos.objects.get(id_estado=1)
        except Glo_Periodos.DoesNotExist:
            return None

        try:
            controlador = Ges_Controlador.objects.get(Q(id=self.kwargs['pk']) & Q(id_periodo=periodo_actual.id))
        except Ges_Controlador.DoesNotExist:
            return None

        id_orden = controlador.nivel_inicial
        self.request.session['id_controlador_real'] = controlador.id

        id_nivel = Ges_Niveles.objects.get(
            Q(id=controlador.id_jefatura.id_nivel_id) & Q(id_periodo=periodo_actual.id))

        try:

            if id_orden == 3:
                count_actividades = Ges_Actividad.objects.values('id_objetivo_tacticotn').filter(
                    id_objetivo_tacticotn=OuterRef('pk')).annotate(
                    count_id_actividad=Count('id', filter=Q(id_periodo=periodo_actual.id)))
                replies2 = Ges_Objetivo_TacticoTN.objects.filter(
                    Q(id_tercer_nivel_id=id_nivel.id_tercer_nivel_id) & Q(id_periodo=periodo_actual.id)).annotate(
                    count_actividades=Subquery(count_actividades.values('count_id_actividad')))

            if id_orden == 2:
                count_actividades = Ges_Actividad.objects.values('id_objetivo_tactico').filter(
                    id_objetivo_tactico=OuterRef('pk')).annotate(
                    count_id_actividad=Count('id', filter=Q(id_periodo=periodo_actual.id)))
                replies2 = Ges_Objetivo_Tactico.objects.filter(
                    Q(id_segundo_nivel_id=id_nivel.id_segundo_nivel_id) & Q(id_periodo=periodo_actual.id)).annotate(
                    count_actividades=Subquery(count_actividades.values('count_id_actividad')))

            if id_orden == 4:
                count_actividades = Ges_Actividad.objects.values('id_objetivo_operativo').filter(
                    id_objetivo_operativo=OuterRef('pk')).annotate(
                    count_id_actividad=Count('id', filter=Q(id_periodo=periodo_actual.id)))
                replies2 = Ges_Objetivo_Operativo.objects.filter(
                    Q(id_cuarto_nivel_id=id_nivel.id_cuarto_nivel_id) & Q(id_periodo=periodo_actual.id)).annotate(

                    count_actividades=Subquery(count_actividades.values('count_id_actividad')))

            context['orden'] = {'orden_nivel': id_orden}
            context['niveles'] = replies2
            context['objetivo'] = id_nivel

            self.request.session['id_orden'] = id_orden

            return context

        except Ges_Jefatura.DoesNotExist:
            context['habilitado'] = {'mensaje': False}


            return None


class SeguimientoActividades(ListView): # Modificado por JR- sprint 8 - OK
    model = Ges_Actividad
    template_name = 'valida_plan/seguimiento_plan_list_actividades.html'

    def get_context_data(self,  **kwargs):
        context = super(SeguimientoActividades, self).get_context_data(**kwargs)
        id_usuario_actual = self.request.user.id  # obtiene id usuario actual

        try:
            periodo_actual = Glo_Periodos.objects.get(id_estado=1)
        except Glo_Periodos.DoesNotExist:
            return None

        self.request.session['id_objetivo']=self.kwargs['pk']#315

        nombre = ""
        if self.request.session['id_orden']==2:
           # lista_actividades = Ges_Actividad.objects.filter(Q(id_objetivo_tactico=self.kwargs['pk']) & Q(id_periodo=periodo_actual.id))

            count_no_vistos = Ges_Observaciones.objects.values('id_actividad_id').filter(id_actividad=OuterRef('pk')).annotate(
              count_id_actividad=Count('id', filter=Q(observado=1) & Q(id_periodo=periodo_actual.id) & (~Q(user_observa=id_usuario_actual))))

            count_observaciones = Ges_Observaciones.objects.values('id_actividad_id').filter(id_actividad=OuterRef('pk')).annotate(
            count_id_actividad=Count('id'))

            lista_actividades = Ges_Actividad.objects.filter(
              Q(id_objetivo_tactico=self.kwargs['pk']) & Q(id_periodo=periodo_actual.id)).annotate(
              count_no_vistos=Subquery(count_no_vistos.values('count_id_actividad')),

                count_observaciones=Subquery(count_observaciones.values('count_id_actividad'))).order_by('-count_no_vistos','-fecha_registro')

            nombre=  Ges_Objetivo_Tactico.objects.get(id=self.kwargs['pk'])

        if self.request.session['id_orden']==3:
           # lista_actividades = Ges_Actividad.objects.filter(Q(id_objetivo_tacticotn=self.kwargs['pk']) & Q(id_periodo=periodo_actual.id))

            count_no_vistos = Ges_Observaciones.objects.values('id_actividad_id').filter(id_actividad=OuterRef('pk')).annotate(
              count_id_actividad=Count('id', filter=Q(observado=1) & Q(id_periodo=periodo_actual.id) & (~Q(user_observa=id_usuario_actual))))
            count_observaciones = Ges_Observaciones.objects.values('id_actividad_id').filter(id_actividad=OuterRef('pk')).annotate(
            count_id_actividad=Count('id'))


            lista_actividades = Ges_Actividad.objects.filter(
              Q(id_objetivo_tacticotn=self.kwargs['pk']) & Q(id_periodo=periodo_actual.id)).annotate(
              count_no_vistos=Subquery(count_no_vistos.values('count_id_actividad')),


                count_observaciones=Subquery(count_observaciones.values('count_id_actividad'))).order_by('-count_no_vistos','-fecha_registro')


            nombre = Ges_Objetivo_TacticoTN.objects.get(id=self.kwargs['pk'])

        if self.request.session['id_orden']==4:

            count_no_vistos = Ges_Observaciones.objects.values('id_actividad_id').filter(id_actividad=OuterRef('pk')).annotate(
              count_id_actividad=Count('id', filter=Q(observado=1) & Q(id_periodo=periodo_actual.id) & (~Q(user_observa=id_usuario_actual))))
            count_observaciones = Ges_Observaciones.objects.values('id_actividad_id').filter(id_actividad=OuterRef('pk')).annotate(
            count_id_actividad=Count('id'))

            lista_actividades = Ges_Actividad.objects.filter(
              Q(id_objetivo_operativo=self.kwargs['pk']) & Q(id_periodo=periodo_actual.id)).annotate(
              count_no_vistos=Subquery(count_no_vistos.values('count_id_actividad')),

                count_observaciones=Subquery(count_observaciones.values('count_id_actividad'))).order_by('-count_no_vistos','-fecha_registro')


            nombre = Ges_Objetivo_Operativo.objects.get(id=self.kwargs['pk'])

        try:
            nivel_usuario = Ges_Jefatura.objects.get(Q(id_user=id_usuario_actual) & Q(id_periodo=periodo_actual.id))
        except Ges_Jefatura.DoesNotExist:
            context['habilitado'] = {'mensaje': False}
            return None


        context['object_list'] = lista_actividades
        context['nombre_objetivo'] = {'nombre': nombre}
        context['id_orden'] = {'id_orden': self.request.session['id_orden']}
        context['id_nivel_controlador']={'id': self.request.session['id_nivel_controlador']}

        #context['objetivo'] = id_nivel


        return context















class ObservacionesListar(ListView): #Modificado por JR- sprint 8 - OK
    model = Ges_Observaciones
    template_name = 'valida_plan/valida_plan_observaciones_list.html'


    def get_context_data(self, **kwargs):
        context = super(ObservacionesListar, self).get_context_data(**kwargs)
        id_actividad = self.kwargs['pk']
        id_usuario_actual = self.request.user.id  # obtiene id usuario actual
        id_objetivo= self.request.session['id_objetivo'] #315
        try:
            periodo_actual = Glo_Periodos.objects.get(id_estado=1)
        except Glo_Periodos.DoesNotExist:
            return None

        try:
            actividad = Ges_Actividad.objects.get(Q(id=id_actividad) & Q(id_periodo=periodo_actual.id))
        except Ges_Actividad.DoesNotExist:
            actividad = 0
            pass

        self.request.session['id_actividad']=id_actividad #27

        lista_observaciones = Ges_Observaciones.objects.filter(Q(id_periodo=periodo_actual.id) & Q(id_actividad=id_actividad)).order_by('-fecha_registro')
        context['object_list'] = lista_observaciones

        context['id_actividad'] = {'id': id_objetivo}
        context['User'] = {'id': id_usuario_actual}
        context['actividad'] = {'descripcion_actividad': actividad.descripcion_actividad}

        return context



class ObservacionesCreate(SuccessMessageMixin, CreateView): # modificado por JR- sprint 8 - ok
    model = Ges_Observaciones
    form_class = ValidaPlanObservacionesForm
    template_name = 'valida_plan/valida_plan_observaciones_form.html'


    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        id_actividad= self.request.session['id_actividad']
        id_usuario_actual = self.request.user.id  # obtiene id usuario actual

        if self.request.session['id_controlador_real'] != None:
            id_controlador_real=self.request.session['id_controlador_real']
        else:
            id_controlador_real=0

        try:
            periodo_activo = Glo_Periodos.objects.get(id_estado=1)
        except Glo_Periodos.DoesNotExist:
            return None

        try:
            usuario_id =  Ges_Jefatura.objects.get(id_user=id_usuario_actual)
        except Ges_Jefatura.DoesNotExist:
            usuario_id = None

        if form.is_valid():
            #form.instance.fecha_inicio= date.today()

            form.instance.id_actividad_id = str(id_actividad)
            form.instance.id_periodo = periodo_activo
            form.instance.user_observa=usuario_id.id_user
            form.instance.observado=1
            form.instance.id_controlador= id_controlador_real
            form.instance.id_objetivo= self.request.session['id_objetivo']
            form.save()
            request.session['message_class'] = "alert alert-success"
            messages.success(self.request, "Los datos fueron creados correctamente!")
            return HttpResponseRedirect('/valida_plan/listaObservacion/' + str(id_actividad))
        else:
            request.session['message_class'] = "alert alert-danger"
            messages.error(self.request, "Error interno: No se ha creado el registro. Comuníquese con el administrador.")
            return HttpResponseRedirect('/valida_plan/listaObservacion/' + str(id_actividad))


class ObservacionDelete(SuccessMessageMixin, DeleteView ): #clase creada por JR- sprint 8 - OK
    model = Ges_Observaciones
    template_name = 'valida_plan/valida_plan_observacion_delete.html'

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        id_actividad = self.request.session['id_actividad']
        try:
            obj.delete()
            request.session['message_class'] = "alert alert-success"
            messages.success(self.request, "El registro fue eliminado correctamente!")
            return HttpResponseRedirect('/valida_plan/listaObservacion/'+str(id_actividad))

        except ProtectedError as e:
            request.session['message_class'] = "alert alert-danger"
            messages.error(request, "Error de integridad: Este nivel posee subniveles los que deben ser borrados antes de borrar este nivel.")
            return HttpResponseRedirect('/valida_plan/listaObservacion/'+str(id_actividad))

        except Exception  as e:
            request.session['message_class'] = "alert alert-danger"
            messages.error(request, "Error interno: No se ha eliminado el registro. Comuníquese con el administrador.")
            return HttpResponseRedirect('/valida_plan/listaObservacion/'+str(id_actividad))



def GestionObservacionesActividades(request, id):
    template_name = "valida_plan/modal_observaciones.html"
    response_data = {}
    ahora = datetime.now()
    fecha = ahora.strftime("%d" + " de " + "%B" + " de " + "%Y" + " a las " + "%H:%M")

    try:
        periodo_activo = Glo_Periodos.objects.get(id_estado=1)
    except Glo_Periodos.DoesNotExist:
        return None

    id_controller = request.session['id_controlador_real']

    try:
        controlador_id = Ges_Controlador.objects.get(id=id_controller)
    except Ges_Controlador.DoesNotExist:
        controlador_id = None

    id_usuario_redacta_plan = controlador_id.id_jefatura
    id_usuario_actual = request.user.id  # obtiene id usuario actual


    try:
        usuario_id = Ges_Jefatura.objects.get(id_user=id_usuario_actual)
    except Ges_Jefatura.DoesNotExist:
        usuario_id = None


    try:
        actividad = Ges_Actividad.objects.get(id=id)
    except Ges_Actividad.DoesNotExist:
        actividad = 0



    var = id_usuario_redacta_plan.id_nivel.orden_nivel  # Nivel del usuario

    if var==2:
        id_objetivo= actividad.id_objetivo_tactico_id
    if var==3:
        id_objetivo = actividad.id_objetivo_tacticotn_id
    if var==4:
        id_objetivo = actividad.id_objetivo_operativo_id


    novacio= Ges_Observaciones.objects.filter(Q(id_actividad=id) & Q(id_periodo=periodo_activo.id) & (~Q(user_observa=id_usuario_actual)))
    #actualiza el estado a leido
    if novacio:

        Ges_Observaciones.objects.filter(Q(id_actividad=id) & Q(id_periodo=periodo_activo.id) & (~Q(user_observa=id_usuario_actual))).update(observado=0,)


    qs = Ges_Observaciones.objects.filter(Q(id_actividad=id) & Q(id_periodo=periodo_activo.id))

    args = {}

    args['id_actividad'] = id
    args['object_list']= qs


    if request.POST.get('action') == 'post':


        observacion = request.POST.get('observacion')

        response_data['observacion'] = observacion
        response_data['id_actividad'] = id
        response_data['fecha'] = fecha


        Ges_Observaciones.objects.create(
            observacion = observacion, id_controlador=id_controller, user_observa= usuario_id.id_user, id_actividad_id=id, id_periodo_id=periodo_activo.id,
           id_objetivo=id_objetivo, observado=1,

            )

        return JsonResponse(response_data)

    return render(request, template_name, args)


def GestionObservacionesObjetivosVp(request, id):
    template_name = "valida_plan/modal_observaciones_objetivos.html"
    response_data = {}


    id_controller = request.session['id_controlador_real']

    try:
        controlador_id = Ges_Controlador.objects.get(id=id_controller)
    except Ges_Controlador.DoesNotExist:
        controlador_id = None

    try:
        periodo_activo = Glo_Periodos.objects.get(id_estado=1)
    except Glo_Periodos.DoesNotExist:
        return None

    id_usuario_redacta_plan= controlador_id.id_jefatura
    id_usuario_actual = request.user.id  # obtiene id usuario actual



    var= id_usuario_redacta_plan.id_nivel.orden_nivel # Nivel del usuario



    if var == 2:
        qs = Ges_Observaciones_sr.objects.filter(Q(id_objetivo_tactico=id) & Q(id_periodo=periodo_activo.id))
    if var == 3:
        qs = Ges_Observaciones_sr.objects.filter(Q(id_objetivo_tactivotn=id) & Q(id_periodo=periodo_activo.id))
    if var == 4:
        qs = Ges_Observaciones_sr.objects.filter(Q(id_objetivo_operativo=id) & Q(id_periodo=periodo_activo.id))


    args = {}

    args['id_objetivo'] = id
    args['object_list']= qs



    return render(request, template_name, args)


def PeriodoActual():
    try:
        periodo_actual = Glo_Periodos.objects.get(id_estado=1)
    except Glo_Periodos.DoesNotExist:
        return None
    return periodo_actual


