from django.contrib.auth.models import User
from django.core import mail
from django.core.mail import EmailMultiAlternatives
from django.db.models import Q, OuterRef, Count, Subquery
from django.shortcuts import render
from django.utils.module_loading import import_string
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from apps.actividades.models import Ges_Actividad
from apps.controlador.models import Ges_Controlador
from apps.estructura.models import Ges_Niveles
from apps.objetivos.models import Ges_Objetivo_Tactico, Ges_Objetivo_TacticoTN, Ges_Objetivo_Operativo
from apps.periodos.models import Glo_Periodos
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib import messages

from apps.registration.models import logEventos
from apps.revision_planificacion.forms import   PlanUpdateForm
from apps.valida_plan.models import Ges_Observaciones
from apps.valida_plan2.models import Ges_Observaciones_sr
from django.conf import settings
from datetime import datetime

class UnidadesListar(ListView):
    model = Ges_Niveles
    template_name = 'revision_planificacion/revision_planificacion_list.html'

    def get_context_data(self, **kwargs):
        context = super(UnidadesListar, self).get_context_data(**kwargs)
        id_usuario_actual = self.request.user.id  # obtiene id usuario actual

        try:
            periodo_actual = Glo_Periodos.objects.get(id_estado=1)
        except Glo_Periodos.DoesNotExist:
            return None

        try:

            count_no_vistos = Ges_Observaciones.objects.values('id_controlador').filter(
                id_controlador=OuterRef('pk')).annotate(
                count_id_actividad=Count('id', filter=Q(observado=1) & Q(id_periodo=periodo_actual.id) & (
                    ~Q(user_observa=id_usuario_actual))))

            count_observaciones = Ges_Observaciones.objects.values('id_controlador').filter(
                id_controlador=OuterRef('pk')).annotate(
                count_id_actividad=Count('id'))

            id_controlador = Ges_Controlador.objects.filter(
                Q(analista_asignado=id_usuario_actual) & Q(id_periodo=periodo_actual.id) & Q(
                    estado_flujo=6)).annotate(
                count_no_vistos=Subquery(count_no_vistos.values('count_id_actividad')),
                count_observaciones=Subquery(count_observaciones.values('count_id_actividad')[0:1])).order_by(
                '-count_no_vistos', '-count_observaciones')

        except Ges_Controlador.DoesNotExist:
            return None

        context['object_list'] = id_controlador
        return context

class ObjetivosListar(ListView):
    model = Ges_Actividad
    template_name = 'revision_planificacion/revision_planificacion_detalle.html'

    def get_context_data(self, **kwargs):
        context = super(ObjetivosListar, self).get_context_data(**kwargs)
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
            if id_orden == 2:
                answer_subquery = Ges_Actividad.objects.values('id_objetivo_tactico_id').filter(
                    id_objetivo_tactico=OuterRef('pk')).annotate(
                    count_actividad=Count('id', filter=Q(id_periodo=periodo_actual.id)))

                count_no_vistos = Ges_Observaciones_sr.objects.values('id_objetivo_tactico').filter(
                    id_objetivo_tactico=OuterRef('pk')).annotate(
                    count_id_actividad=Count('id', filter=Q(observado=1) & Q(id_periodo=periodo_actual.id) & (
                        ~Q(user_observa=id_usuario_actual))))

                count_observaciones = Ges_Observaciones_sr.objects.values('id_objetivo_tactico').filter(
                    id_objetivo_tactico=OuterRef('pk')).annotate(
                    count_id_actividad=Count('id'))

                replies2 = Ges_Objetivo_Tactico.objects.filter(
                    Q(id_segundo_nivel_id=id_nivel.id_segundo_nivel_id) & Q(id_periodo=periodo_actual.id)).annotate(
                    count_no_vistos=Subquery(count_no_vistos.values('count_id_actividad')),
                    count_observaciones=Subquery(count_observaciones.values('count_id_actividad')),
                    count_actividad=Subquery(answer_subquery.values('count_actividad')[0:1])).order_by(
                    '-count_no_vistos', '-count_observaciones')

            if id_orden == 3:
                answer_subquery = Ges_Actividad.objects.values('id_objetivo_tacticotn_id').filter(
                    id_objetivo_tacticotn=OuterRef('pk')).annotate(
                    count_actividad=Count('id', filter=Q(id_periodo=periodo_actual.id)))

                count_no_vistos = Ges_Observaciones_sr.objects.values('id_objetivo_tacticotn').filter(
                    id_objetivo_tacticotn=OuterRef('pk')).annotate(
                    count_id_actividad=Count('id', filter=Q(observado=1) & Q(id_periodo=periodo_actual.id) & (
                        ~Q(user_observa=id_usuario_actual))))

                count_observaciones = Ges_Observaciones_sr.objects.values('id_objetivo_tacticotn').filter(
                    id_objetivo_tacticotn=OuterRef('pk')).annotate(
                    count_id_actividad=Count('id'))

                replies2 = Ges_Objetivo_TacticoTN.objects.filter(
                    Q(id_tercer_nivel_id=id_nivel.id_tercer_nivel_id) & Q(id_periodo=periodo_actual.id)).annotate(
                    count_no_vistos=Subquery(count_no_vistos.values('count_id_actividad')),
                    count_observaciones=Subquery(count_observaciones.values('count_id_actividad')),
                    count_actividad=Subquery(answer_subquery.values('count_actividad')[0:1])).order_by(
                    '-count_no_vistos', '-count_observaciones')

            if id_orden == 4:
                answer_subquery = Ges_Actividad.objects.values('id_objetivo_operativo_id').filter(
                    id_objetivo_operativo=OuterRef('pk')).annotate(
                    count_actividad=Count('id', filter=Q(id_periodo=periodo_actual.id)))

                count_no_vistos = Ges_Observaciones_sr.objects.values('id_objetivo_operativo').filter(
                    id_objetivo_operativo=OuterRef('pk')).annotate(
                    count_id_actividad=Count('id', filter=Q(observado=1) & Q(id_periodo=periodo_actual.id) & (
                        ~Q(user_observa=id_usuario_actual))))

                count_observaciones = Ges_Observaciones_sr.objects.values('id_objetivo_operativo').filter(
                    id_objetivo_operativo=OuterRef('pk')).annotate(
                    count_id_actividad=Count('id'))

                replies2 = Ges_Objetivo_Operativo.objects.filter(
                    Q(id_cuarto_nivel_id=id_nivel.id_cuarto_nivel_id) & Q(id_periodo=periodo_actual.id)).annotate(
                    count_no_vistos=Subquery(count_no_vistos.values('count_id_actividad')),
                    count_observaciones=Subquery(count_observaciones.values('count_id_actividad')),
                    count_actividad=Subquery(answer_subquery.values('count_actividad')[0:1])).order_by(
                    '-count_no_vistos', '-count_observaciones')

        except:
            return None
        context['orden'] = {'orden_nivel': id_orden}
        context['niveles'] = replies2
        context['objetivo'] = id_nivel
        self.request.session['id_orden'] = id_orden
        return context

class ActividadesListar(ListView):
    model = Ges_Actividad
    template_name = 'revision_planificacion/revision_planificacion_actividades.html'

    def get_context_data(self,  **kwargs):
        context = super(ActividadesListar, self).get_context_data(**kwargs)
        id_usuario_actual = self.request.user.id  # obtiene id usuario actual
        try:
            periodo_actual = Glo_Periodos.objects.get(id_estado=1)
        except Glo_Periodos.DoesNotExist:
            return None

        self.request.session['id_objetivo']=self.kwargs['pk']

        nombre = ""
        try:
            if self.request.session['id_orden']==2:
               # lista_actividades = Ges_Actividad.objects.filter(Q(id_objetivo_tactico=self.kwargs['pk']) & Q(id_periodo=periodo_actual.id))

                count_no_vistos = Ges_Observaciones.objects.values('id_actividad_id').filter(
                   id_actividad=OuterRef('pk')).annotate(
                   count_id_actividad=Count('id', filter=Q(observado=1) & Q(id_periodo=periodo_actual.id) & (
                       ~Q(user_observa=id_usuario_actual))))

                count_observaciones = Ges_Observaciones.objects.values('id_actividad').filter(id_actividad=OuterRef('pk')).annotate(
                count_id_actividad=Count('id'))

                lista_actividades = Ges_Actividad.objects.filter(
                  Q(id_objetivo_tactico=self.kwargs['pk']) & Q(id_periodo=periodo_actual.id)).annotate(count_no_vistos=Subquery(count_no_vistos.values('count_id_actividad')),
                 count_observaciones=Subquery(count_observaciones.values('count_id_actividad'))).order_by('-count_observaciones')

                nombre=  Ges_Objetivo_Tactico.objects.get(id=self.kwargs['pk'])

            if self.request.session['id_orden']==3:
               # lista_actividades = Ges_Actividad.objects.filter(Q(id_objetivo_tacticotn=self.kwargs['pk']) & Q(id_periodo=periodo_actual.id))

                count_no_vistos = Ges_Observaciones.objects.values('id_actividad_id').filter(
                   id_actividad=OuterRef('pk')).annotate(
                   count_id_actividad=Count('id', filter=Q(observado=1) & Q(id_periodo=periodo_actual.id) & (
                       ~Q(user_observa=id_usuario_actual))))

                count_observaciones = Ges_Observaciones.objects.values('id_actividad').filter(id_actividad=OuterRef('pk')).annotate(
                count_id_actividad=Count('id'))

                lista_actividades = Ges_Actividad.objects.filter(
                  Q(id_objetivo_tacticotn=self.kwargs['pk']) & Q(id_periodo=periodo_actual.id)).annotate(count_no_vistos=Subquery(count_no_vistos.values('count_id_actividad')),
                 count_observaciones=Subquery(count_observaciones.values('count_id_actividad'))).order_by('-count_observaciones')


                nombre = Ges_Objetivo_TacticoTN.objects.get(id=self.kwargs['pk'])

            if self.request.session['id_orden']==4:


                count_observaciones = Ges_Observaciones.objects.values('id_actividad').filter(id_actividad=OuterRef('pk')).annotate(
                count_id_actividad=Count('id'))

                count_no_vistos = Ges_Observaciones.objects.values('id_actividad_id').filter(
                    id_actividad=OuterRef('pk')).annotate(
                    count_id_actividad=Count('id', filter=Q(observado=1) & Q(id_periodo=periodo_actual.id) & (
                        ~Q(user_observa=id_usuario_actual))))

                lista_actividades = Ges_Actividad.objects.filter(
                  Q(id_objetivo_operativo=self.kwargs['pk']) & Q(id_periodo=periodo_actual.id)).annotate(count_no_vistos=Subquery(count_no_vistos.values('count_id_actividad')),
                 count_observaciones=Subquery(count_observaciones.values('count_id_actividad'))).order_by('-count_observaciones')
                nombre = Ges_Objetivo_Operativo.objects.get(id=self.kwargs['pk'])
        except:
            return None



        context['object_list'] = lista_actividades

        context['nombre_objetivo'] = {'nombre': nombre}
        context['id_orden'] = {'id_orden': self.request.session['id_orden']}


        context['id_nivel_controlador']={'id': self.request.session['id_nivel_controlador']}


        return context

class RechazaPlan(UpdateView):
    model = Ges_Controlador
    form_class = PlanUpdateForm
    template_name = 'revision_planificacion/revision_planificacion_rechaza_form.html'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        id_controlador = kwargs['pk']
        id_usuario_actual = self.request.user.id  # obtiene id usuario actual


        try:
            periodo_actual = Glo_Periodos.objects.get(id_estado=1)
        except Glo_Periodos.DoesNotExist:
            return None

        controladorPlan = self.model.objects.get(id=id_controlador)
        email_jefatura = controladorPlan.id_jefatura.id_user.email    #correo de rechazo
        email_jefatura_primera = controladorPlan.jefatura_primerarevision.id_user.email    #correo de rechazo 1era revision

        try:
            email_jefatura_segunda = controladorPlan.jefatura_segundarevision.id_user.email  # correo de rechazo 2da revision
        except:
            email_jefatura_segunda = None
            pass

        lista_observaciones = int(Ges_Observaciones_sr.objects.filter(Q(id_controlador=id_controlador) & Q(id_periodo=periodo_actual.id)
                                                         & Q(observado=1) & Q(user_observa=id_usuario_actual)).count() ) + int(Ges_Observaciones.objects.filter(
            Q(id_controlador=id_controlador) & Q(id_periodo=periodo_actual.id)
            & Q(observado=1) & Q(user_observa=id_usuario_actual)).count())


        #instancia_nivel = self.model.objects.get(id=id_controlador)
        #form = self.form_class(request.POST, instance=instancia_nivel)
        estado = 11
        controladorPlan.estado_flujo_id = int(estado)
        if int(lista_observaciones) > 0:
            try:
                controladorPlan.save()
                idcorreoJefatura = [email_jefatura, email_jefatura_primera, email_jefatura_segunda]
                subject = 'Plan Rechazado ' + controladorPlan.id_jefatura.id_nivel.descripcion_nivel
                message = 'Estimada(o) Usuaria(o), Su plan fue rechazado con observaciones.  Atte. Subdpto. de Planificación Institucional.>Correo generado automaticamente no responder.'
                messageHtml = 'Estimada(o) Usuaria(o),<br> Su plan fue rechazado con observaciones. <br> Atte. <br>Subdpto. de Planificación Institucional.<br><p style="font-size:12px;color:red;">correo generado automaticamente favor no responder.'
               # send_correo(idcorreoJefatura, subject, message, messageHtml)


                tipo_evento = "Rechaza plan Analista"
                metodo = "Revisión - Planificación"
                usuario_evento = self.request.user
                jefatura_dirigida = None
                logEventosCreate(tipo_evento, metodo, usuario_evento, jefatura_dirigida)
                request.session['message_class'] = "alert alert-success"
                messages.success(self.request,
                                 "El plan fue rechazado correctamente y enviado a la jefatura que lo formuló para su corrección.")
                return HttpResponseRedirect('/revision_planificacion/listarUnidadesAnalista')
            except:
                request.session['message_class'] = "alert alert-danger"
                messages.error(self.request,
                               "Error interno: El plan no fue rechazado, intente nuevamente o comuníquese con el administrador.")
                return HttpResponseRedirect('/revision_planificacion/listarUnidadesAnalista')
        else:
            request.session['message_class'] = "alert alert-danger"
            messages.error(self.request, "Debe ingresar al menos una observacion para rechazar el plan.")
            return HttpResponseRedirect('/revision_planificacion/listarUnidadesAnalista')



class AceptaPlan(UpdateView):
    model = Ges_Controlador
    form_class = PlanUpdateForm
    template_name = 'revision_planificacion/revision_planificacion_acepta_form.html'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        id_controlador = kwargs['pk']
        id_usuario_actual = self.request.user.id

        try:
            periodo_actual = Glo_Periodos.objects.get(id_estado=1)
        except Glo_Periodos.DoesNotExist:
            return None

        controladorPlan = self.model.objects.get(Q(id=id_controlador) & Q(id_periodo=periodo_actual.id))
        #Se debe cambiar por email Analistas
        email_jefatura = controladorPlan.id_jefatura.id_user.email  # correo de rechazo
        email_jefatura_primera = controladorPlan.jefatura_primerarevision.id_user.email  # correo de rechazo 1era revision

        try:
            email_jefatura_segunda = controladorPlan.jefatura_segundarevision.id_user.email  # correo de rechazo 2da revision
        except:
            email_jefatura_segunda = None
            pass


        #instancia_nivel = self.model.objects.get(id=id_controlador)
        #form = self.form_class(request.POST, instance=controladorPlan)
        estado = 7
        controladorPlan.estado_flujo_id = int(estado)
        try:
            controladorPlan.save()

            idcorreoJefatura = [email_jefatura, email_jefatura_primera, email_jefatura_segunda]
            subject = 'Plan Aceptado ' + controladorPlan.id_jefatura.id_nivel.descripcion_nivel
            message = 'Estimada(o) Usuaria(o), Su plan enviado para revisión fue aceptado por el Subdpto de Planificación Institucional.  Atte. Subdpto. de Planificación Institucional.>Correo generado automaticamente no responder.'
            messageHtml = 'Estimada(o) Usuaria(o),<br> Su plan enviado para revisión fue aceptado por el Subdpto de Planificación Institucional. <br> Atte. <br>Subdpto. de Planificación Institucional.<br><p style="font-size:12px;color:red;">correo generado automaticamente favor no responder.'
            # send_correo(idcorreoJefatura, subject, message, messageHtml)

            tipo_evento = "Aprueba plan Analista"
            metodo = "Revisión - Planificación"
            usuario_evento = self.request.user
            jefatura_dirigida = None
            logEventosCreate(tipo_evento, metodo, usuario_evento, jefatura_dirigida)
            request.session['message_class'] = "alert alert-success"
            messages.success(self.request, "El plan fue aceptado correctamente.")
            return HttpResponseRedirect('/revision_planificacion/listarUnidadesAnalista')
        except:
            request.session['message_class'] = "alert alert-danger"
            messages.error(self.request,
                           "Error interno: El plan no ha podido ser aceptado. Comuníquese con el administrador.")
            return HttpResponseRedirect('/revision_planificacion/listarUnidadesAnalista')


def GestionObservacionesActividades(request, id):
    template_name = "revision_planificacion/modal_observaciones_actividad.html"
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
        usuario_id = User.objects.get(id=id_usuario_actual)
    except User.DoesNotExist:
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
            observacion = observacion, id_controlador=id_controller, user_observa= usuario_id, id_actividad_id=id, id_periodo_id=periodo_activo.id,
           id_objetivo=id_objetivo, observado=1,

            )


        return JsonResponse(response_data)

    return render(request, template_name, args)


def GestionObservacionesObjetivosVp2(request, id):
    template_name = "revision_planificacion/modal_observaciones_objetivos_Analista.html"
    response_data = {}
    ahora = datetime.now()
    fecha = ahora.strftime("%d" + " de " + "%B" + " de " + "%Y" + " a las " + "%H:%M")

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

    try:
        usuario_id = User.objects.get(id=id_usuario_actual)
    except User.DoesNotExist:
        usuario_id = None

    var= id_usuario_redacta_plan.id_nivel.orden_nivel # Nivel del usuario

    # actualiza el estado a leido
    if var == 2:
        novacio= Ges_Observaciones_sr.objects.filter(
            Q(id_objetivo_tactico=id) & Q(id_periodo=periodo_activo.id) & (~Q(user_observa = id_usuario_actual)))
        if novacio:
            Ges_Observaciones_sr.objects.filter(Q(id_objetivo_tactico=id) & Q(id_periodo=periodo_activo.id) & (~Q(user_observa = id_usuario_actual))).update(
                observado=0,
            )
    if var == 3:
        novacio = Ges_Observaciones_sr.objects.filter(
            Q(id_objetivo_tacticotn=id) & Q(id_periodo=periodo_activo.id)  & (~Q(user_observa = id_usuario_actual)))
        if novacio:
            Ges_Observaciones_sr.objects.filter(Q(id_objetivo_tacticotn=id) & Q(id_periodo=periodo_activo.id) & (~Q(user_observa = id_usuario_actual))).update(
                observado=0,
            )
    if var == 4:
        novacio = Ges_Observaciones_sr.objects.filter(
            Q(id_objetivo_operativo=id) & Q(id_periodo=periodo_activo.id)  & (~Q(user_observa = id_usuario_actual)))
        if novacio:
            Ges_Observaciones_sr.objects.filter(Q(id_objetivo_operativo=id) & Q(id_periodo=periodo_activo.id) & (~Q(user_observa = id_usuario_actual))).update(
                observado=0,
            )

    if var == 2:
        qs = Ges_Observaciones_sr.objects.filter(Q(id_objetivo_tactico=id) & Q(id_periodo=periodo_activo.id))
    if var == 3:
        qs = Ges_Observaciones_sr.objects.filter(Q(id_objetivo_tactivotn=id) & Q(id_periodo=periodo_activo.id))
    if var == 4:
        qs = Ges_Observaciones_sr.objects.filter(Q(id_objetivo_operativo=id) & Q(id_periodo=periodo_activo.id))


    args = {}

    args['id_objetivo'] = id
    args['object_list']= qs


    if request.POST.get('action') == 'post':


        observacion = request.POST.get('observacion')

        response_data['observacion'] = observacion
        response_data['id_actividad'] = id
        response_data['fecha'] = fecha

        if var == 2:
            Ges_Observaciones_sr.objects.create(
                observacion=observacion, id_controlador=id_controller, user_observa=usuario_id,
                id_objetivo_tactico_id=id, id_periodo_id=periodo_activo.id, observado=1,
            )
        if var == 3:
            Ges_Observaciones_sr.objects.create(
                observacion=observacion, id_controlador=id_controller, user_observa=usuario_id,
                id_objetivo_tacticotn_id=id, id_periodo_id=periodo_activo.id, observado=1,
            )
        if var == 4:
            Ges_Observaciones_sr.objects.create(
                observacion=observacion, id_controlador=id_controller, user_observa=usuario_id,
                id_objetivo_operativo_id=id, id_periodo_id=periodo_activo.id, observado=1,
            )



        return JsonResponse(response_data)

    return render(request, template_name, args)


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

def logEventosCreate(tipo_evento, metodo ,usuario_evento, jefatura_dirigida):
    logEventos.objects.create(
        tipo_evento=tipo_evento,
        metodo=metodo,
        usuario_evento=usuario_evento,
        jefatura_dirigida=jefatura_dirigida,
    )
    return None








