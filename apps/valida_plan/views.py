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
from decimal import *
from django.db.models import Sum
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
from apps.gestion_horas.models import Ges_Registro_Horas
from apps.eje.models import Ges_Ejes
from django.contrib import messages
from django.core.mail import EmailMessage,send_mass_mail



def EnviarCorreoRechazo_formulador(email_jefatura):
    # try:
    #     periodo_actual = Glo_Periodos.objects.get(id_estado=1)
    # except Glo_Periodos.DoesNotExist:
    #     return None

    #controladorPlan = Ges_Jefatura.objects.values_list('id_user__email' , flat=True).filter(Q(id_periodo=periodo_actual) & Q(id=id_jefatura))
    idcorreoJefatura=[str(email_jefatura)]

    subject = 'Rechazo Plan de Gestión '
    messageHtml = 'Estimada(o) Usuaria(o),<br> El plan de gestión enviado a revisión fue rechazado por su jefatura, para mayor información ingrese al sitio Capacity Institucional y revise las observaciones realizadas. <br> Atte. <br>Subdpto. de Planificación Institucional.<br><p style="font-size:12px;color:red;">correo generado automaticamente favor no responder.'

    email = EmailMessage(subject, messageHtml ,to=idcorreoJefatura)

    email.content_subtype='html'
    email.send()



def EnviarCorreoRechazo_primera_jefatura(email_jefatura, area_plan):
    # try:
    #     periodo_actual = Glo_Periodos.objects.get(id_estado=1)
    # except Glo_Periodos.DoesNotExist:
    #     return None

    ahora = datetime.now()
    fecha = ahora.strftime("%d" + "/" + "%m" + "/" + "%Y" + " a las " + "%H:%M")

    #controladorPlan = Ges_Jefatura.objects.values_list('id_user__email' , flat=True).filter(Q(id_periodo=periodo_actual) & Q(id=id_jefatura))
    idcorreoJefatura=[str(email_jefatura)]
    area_plan=str(area_plan)

    subject = 'Rechazo Plan de Gestión '
    messageHtml = 'Estimada(o) Usuaria(o),<br> Se informa que con fecha <b>'+ fecha +'</b> se ha rechazado el plan de gestión para correpondiente a <b>' + area_plan + '</b> . <br> Atte. <br>Subdpto. de Planificación Institucional.<br><p style="font-size:12px;color:red;">correo generado automaticamente favor no responder.'

    email = EmailMessage(subject, messageHtml ,to=idcorreoJefatura)

    email.content_subtype='html'
    email.send()


def EnviarCorreoAcepta_formulador(email_jefatura):
    # try:
    #     periodo_actual = Glo_Periodos.objects.get(id_estado=1)
    # except Glo_Periodos.DoesNotExist:
    #     return None

    #controladorPlan = Ges_Jefatura.objects.values_list('id_user__email' , flat=True).filter(Q(id_periodo=periodo_actual) & Q(id=id_jefatura))

    ahora = datetime.now()
    fecha = ahora.strftime("%d" + "/" + "%m" + "/" + "%Y" + " a las " + "%H:%M")

    idcorreoJefatura=[str(email_jefatura)]

    subject = 'Aprobación Plan de Gestión '
    messageHtml = 'Estimada(o) Usuaria(o),<br> Se informa que con fecha <b>'+ fecha +'</b> el plan de gestión fue aprobado por su jefatura y enviado a revisión. <br> Atte. <br>Subdpto. de Planificación Institucional.<br><p style="font-size:12px;color:red;">correo generado automaticamente favor no responder.'

    email = EmailMessage(subject, messageHtml ,to=idcorreoJefatura)

    email.content_subtype='html'
    email.send()



def EnviarCorreoAcepta_primera_jefatura(email_jefatura, area_plan):
    # try:
    #     periodo_actual = Glo_Periodos.objects.get(id_estado=1)
    # except Glo_Periodos.DoesNotExist:
    #     return None

    ahora = datetime.now()
    fecha = ahora.strftime("%d" + "/" + "%m" + "/" + "%Y" + " a las " + "%H:%M")

    #controladorPlan = Ges_Jefatura.objects.values_list('id_user__email' , flat=True).filter(Q(id_periodo=periodo_actual) & Q(id=id_jefatura))
    idcorreoJefatura=[str(email_jefatura)]
    area_plan=str(area_plan)

    subject = 'Aprobación Plan de Gestión '
    messageHtml = 'Estimada(o) Usuaria(o),<br> Se informa que con fecha <b>'+ fecha +'</b> ha aprobado y enviado a revisión el plan de gestión correpondiente a <b>' + area_plan + '</b>. <br> Atte. <br>Subdpto. de Planificación Institucional.<br><p style="font-size:12px;color:red;">correo generado automaticamente favor no responder.'

    email = EmailMessage(subject, messageHtml ,to=idcorreoJefatura)

    email.content_subtype='html'
    email.send()

class RechazaPlan(UpdateView):
    model = Ges_Controlador
    form_class = RechazaPlanUpdateForm
    template_name = 'valida_plan/valida_plan_rechaza_form.html'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        id_controlador = kwargs['pk']
        email_primera_jefatura = self.request.user.email  # obtiene id usuario actual
        area_plan= Ges_Controlador.objects.get(id=id_controlador)
        area_plan= area_plan.id_jefatura.id_nivel
        id_usuario_actual = self.request.user.id

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

        instancia_nivel = self.model.objects.get(Q(id=id_controlador) & Q(id_periodo=periodo_actual.id))
        form = self.form_class(request.POST, instance=instancia_nivel)

        count_obs_no_vistas= Ges_Observaciones.objects.filter(Q(id_controlador=id_controlador ) & Q(observado=1) & ~Q(user_observa_id = id_usuario_actual) & Q(id_periodo=periodo_actual.id)).count()
        count_obs_no_vistas_generales = Ges_Observaciones_sr.objects.filter(
            Q(id_controlador=id_controlador) & Q(observado=1) & ~Q(user_observa_id=id_usuario_actual) & Q(id_periodo=periodo_actual.id)).count()


        count_obs_nuevas= Ges_Observaciones.objects.filter(Q(id_controlador=id_controlador ) & Q(observado=1) & Q(user_observa_id = id_usuario_actual) & Q(id_periodo=periodo_actual.id)).count()
        count_obs_nuevas_generales = Ges_Observaciones_sr.objects.filter(
            Q(id_controlador=id_controlador) & Q(observado=1) & Q(user_observa_id=id_usuario_actual) & Q(id_periodo=periodo_actual.id)).count()

        if count_obs_no_vistas == 0 and count_obs_no_vistas_generales == 0:
            if count_obs_nuevas > 0 or count_obs_nuevas_generales > 0:
                if form.is_valid():
                    form.save()

                    try:

                        EnviarCorreoRechazo_formulador(email_jefatura)
                        EnviarCorreoRechazo_primera_jefatura(email_primera_jefatura, area_plan)
                        request.session['message_class'] = "alert alert-success"  # Tipo mensaje
                        messages.success(request,
                                         "El Plan fue rechazado correctamente y el correo de notificación fue enviado a quien formuló el plan!.")  # mensaje
                        return HttpResponseRedirect('/valida_plan/listarUnidades')  # Redirije a la pantalla principal

                    except:

                        request.session['message_class'] = "alert alert-warning"  # Tipo mensaje
                        messages.success(request,
                                         "El Plan fue rechazado correctamente!, pero el servicio de correo tuvo un inconveniente favor comuníquese con su la jefatura que redactó el plan para informarle del rechazo.")  # mensaje
                        return HttpResponseRedirect('/valida_plan/listarUnidades')  # Redirije a la pantalla principal


                else:
                    request.session['message_class'] = "alert alert-danger"
                    messages.error(self.request,
                                   "Error interno: El plan no ha podido ser rechazado. Comuníquese con el administrador.")
                    return HttpResponseRedirect('/valida_plan/listarUnidades')
            else:
                request.session['message_class'] = "alert alert-danger"
                messages.error(self.request,
                               "Para rechazar el plan, primero debe ingresar al menos una observación.")
                return HttpResponseRedirect('/valida_plan/listarUnidades')
        else:
            request.session['message_class'] = "alert alert-danger"
            messages.error(self.request,
                           "Para rechazar el plan, primero debe leer todas las observaciones.")
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
                id_jef_final=0

        kwargs['nivel_jefatura'] = id_jef_final

        return kwargs

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        id_nivel = kwargs['pk'] #id del controlador
        id_nivel = int(id_nivel)
        instancia_nivel = self.model.objects.get(id=id_nivel)
        id_jefatura = request.POST['jefatura_segundarevision']
        id_jefatura_solicita = request.POST['id_jefatura']
        id_usuario_actual = self.request.user.id

        try:
            periodo_actual = Glo_Periodos.objects.get(id_estado=1)
        except Glo_Periodos.DoesNotExist:
            return None


        email_primera_jefatura = self.request.user.email  # obtiene id usuario actual
        area_plan= Ges_Controlador.objects.get(Q(id=id_nivel) & Q(id_periodo=periodo_actual.id))
        email_jefatura = area_plan.id_jefatura.id_user.email

        area_plan= area_plan.id_jefatura.id_nivel


        try:
            periodo_actual = Glo_Periodos.objects.get(id_estado=1)
        except Glo_Periodos.DoesNotExist:
            return None

        count_obs_no_vistas= Ges_Observaciones.objects.filter(Q(id_controlador=id_nivel ) & Q(observado=1) & ~Q(user_observa_id = id_usuario_actual)).count()
        count_obs_no_vistas_generales = Ges_Observaciones_sr.objects.filter(
            Q(id_controlador=id_nivel) & Q(observado=1) & ~Q(user_observa_id=id_usuario_actual)).count()




        if count_obs_no_vistas == 0 and count_obs_no_vistas_generales == 0:
            if int(id_jefatura) != 0:

                id_nivel_post = Ges_Jefatura.objects.get(id=id_jefatura)
                id_nivel_post = id_nivel_post.id_nivel_id

                form = self.form_class(id_nivel_post, request.POST, instance=instancia_nivel)

                idcorreoJefaturaOb = Ges_Jefatura.objects.get(id=id_jefatura)

                nivel_usuario = Ges_Jefatura.objects.get(Q(id_user=id_usuario_actual) & Q(id_periodo=periodo_actual.id))

                if form.is_valid():
                    form.save()
                    d_jefatura = Ges_Jefatura.objects.get(id_user=id_usuario_actual)
                    update_state(id_jefatura_solicita, id_jefatura, 5, d_jefatura.id)
                    tipo_evento = "Envío Plan a segunda revisión."
                    metodo = "Controlador - AceptaPlan"
                    usuario_evento = nivel_usuario.id_user
                    jefatura_dirigida = idcorreoJefaturaOb.id_user
                    logEventosCreate(tipo_evento, metodo, usuario_evento, jefatura_dirigida)

                    try:

                        EnviarCorreoAcepta_formulador(email_jefatura)
                        EnviarCorreoAcepta_primera_jefatura(email_primera_jefatura, area_plan)

                        request.session['message_class'] = "alert alert-success"  # Tipo mensaje
                        messages.success(request,
                                         "El Plan ha sido aceptado correctamente y el correo de notificación fue enviado a quien formuló el plan!.")  # mensaje
                        return HttpResponseRedirect('/valida_plan/listarUnidades')  # Redirije a la pantalla principal

                    except:

                        request.session['message_class'] = "alert alert-warning"  # Tipo mensaje
                        messages.success(request,
                                         "El Plan fue aceptado correctamente!, pero el servicio de correo tuvo un inconveniente favor comuníquese con su la jefatura que redactó el plan para informarle del rechazo.")  # mensaje
                        return HttpResponseRedirect('/valida_plan/listarUnidades')  # Redirije a la pantalla principal


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

                try:

                    EnviarCorreoAcepta_formulador(email_jefatura)
                    EnviarCorreoAcepta_primera_jefatura(email_primera_jefatura, area_plan)

                    request.session['message_class'] = "alert alert-success"  # Tipo mensaje
                    messages.success(request,
                                     "El Plan ha sido aceptado y enviado a validación de planificación!, el correo de notificación fue enviado a quien formuló el plan!.")  # mensaje
                    return HttpResponseRedirect('/valida_plan/listarUnidades')  # Redirije a la pantalla principal

                except:

                    request.session['message_class'] = "alert alert-warning"  # Tipo mensaje
                    messages.success(request,
                                     "El Plan ha sido aceptado y enviado a validación de planificación!, pero el servicio de correo tuvo un inconveniente favor comuníquese con su la jefatura que redactó el plan para informarle del rechazo.")  # mensaje
                    return HttpResponseRedirect('/valida_plan/listarUnidades')  # Redirije a la pantalla principal

                # request.session['message_class'] = "alert alert-success"
                # messages.success(self.request, "Estimado Usuario:: El plan ha sido enviado correctamente a planificación para su revisión.")
                # return HttpResponseRedirect('/valida_plan/listarUnidades')
        else:
            request.session['message_class'] = "alert alert-danger"
            messages.error(self.request,
                           "Estimado usuario, para enviar el plan debe leer todas las observaciones relacionadas.")
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

            count_no_vistos_generales = Ges_Observaciones_sr.objects.values('id_controlador').filter(
                id_controlador=OuterRef('pk')).annotate(
                count_id_actividad=Count('id', filter=Q(observado=1) & Q(id_periodo=periodo_actual.id) & (
                    ~Q(user_observa=id_usuario_actual))))

            count_observaciones = Ges_Observaciones.objects.values('id_controlador').filter(
                id_controlador=OuterRef('pk')).annotate(
                count_id_actividad=Count('id'))


            id_controlador = Ges_Controlador.objects.filter(
                Q(jefatura_primerarevision=id_jefatura.id) & Q(id_periodo=periodo_actual.id) & Q(estado_flujo=4)).annotate(
                count_no_vistos=Subquery(count_no_vistos.values('count_id_actividad')),
                count_no_vistos_generales=Subquery(count_no_vistos_generales.values('count_id_actividad')),
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

        self.request.session['id_controlador_uformula']=controlador.id

        try:

            total_dias = list(Ges_Registro_Horas.objects.filter(
                Q(id_nivel=controlador.id_jefatura.id_nivel_id) & Q(id_periodo=periodo_actual.id)).aggregate(
                Sum('dias_habiles')).values())[0]

            total_utilizado = list(Ges_Actividad.objects.filter(
                Q(id_controlador=controlador.id) & Q(id_periodo=periodo_actual.id)).aggregate(
                Sum('total_horas')).values())[0]

            if total_dias != None:
                total_horas = total_dias * 8
            else:
                total_horas = 0

            if total_utilizado != None:
                consumidas = total_utilizado
                total_utilizado = total_horas - total_utilizado
                try:
                    avance_porcentaje = (consumidas / total_horas) * 100
                    avance_porcentaje = Decimal(avance_porcentaje)
                    avance_porcentaje = avance_porcentaje.quantize(Decimal('0.1'), rounding=ROUND_UP)
                except ZeroDivisionError:
                    avance_porcentaje = 0

            else:
                total_utilizado = total_horas
                consumidas = 0
                avance_porcentaje = 0
            total_utilizado = int(total_utilizado)
            consumidas = int(consumidas)

        except Ges_Registro_Horas.DoesNotExist:
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
                count_no_vistos = Ges_Observaciones.objects.values('id_objetivo').filter(Q(
                    id_objetivo=OuterRef('pk')) ).annotate(
                    count_id_actividad=Count('id', filter=Q(observado=1) & Q(id_controlador=controlador.id) & Q(id_periodo=periodo_actual.id) & (~Q(user_observa=id_usuario_actual))))

                count_observaciones = Ges_Observaciones.objects.values('id_objetivo').filter(Q(
                    id_objetivo=OuterRef('pk')) ).annotate(
                    count_id_actividad=Count('id', filter=Q(id_periodo=periodo_actual.id) & Q(id_controlador=controlador.id)))

                count_actividades = Ges_Actividad.objects.values('id_objetivo_tacticotn').filter(
                    id_objetivo_tacticotn=OuterRef('pk')).annotate(
                    count_id_actividad=Count('id', filter=Q(id_periodo=periodo_actual.id) & Q(id_controlador=controlador.id)))

                count_no_vistos_obj = Ges_Observaciones_sr.objects.values('id_objetivo_tacticotn').filter(
                    id_objetivo_tacticotn=OuterRef('pk')).annotate(
                    count_id_actividad=Count('id', filter=Q(observado=1) & Q(id_controlador=controlador.id) & Q(id_periodo=periodo_actual.id) & (
                        ~Q(user_observa=id_usuario_actual))))

                count_observaciones_obj = Ges_Observaciones_sr.objects.values('id_objetivo_tacticotn').filter(
                    id_objetivo_tacticotn=OuterRef('pk')).annotate(
                    count_id_actividad=Count('id', Q(id_periodo=periodo_actual.id) & Q(id_controlador=controlador.id)))

                replies2 = Ges_Objetivo_TacticoTN.objects.filter(
                    Q(id_tercer_nivel_id=id_nivel.id_tercer_nivel_id) & Q(id_periodo=periodo_actual.id)).annotate(
                    count_no_vistos=Subquery(count_no_vistos.values('count_id_actividad')),
                    count_actividades=Subquery(count_actividades.values('count_id_actividad')),
                    count_no_vistos_obj=Subquery(count_no_vistos_obj.values('count_id_actividad')),
                    count_observaciones_obj=Subquery(count_observaciones_obj.values('count_id_actividad')),
                    count_observaciones=Subquery(count_observaciones.values('count_id_actividad'))).order_by(
                    '-count_no_vistos', '-count_observaciones')


            if id_orden == 2:
               # replies2 = Ges_Objetivo_Tactico.objects.filter(id_segundo_nivel_id=id_nivel.id_segundo_nivel_id)
                count_no_vistos = Ges_Observaciones.objects.values('id_objetivo').filter(Q(
                    id_objetivo=OuterRef('pk')) ).annotate(
                    count_id_actividad=Count('id', filter=Q(observado=1) & Q(id_controlador=controlador.id) & Q(id_periodo=periodo_actual.id) & (~Q(user_observa=id_usuario_actual))))

                count_observaciones = Ges_Observaciones.objects.values('id_objetivo').filter(Q(
                    id_objetivo=OuterRef('pk'))).annotate(
                    count_id_actividad=Count('id' , filter=Q(id_periodo=periodo_actual.id) & Q(id_controlador=controlador.id)))

                count_actividades = Ges_Actividad.objects.values('id_objetivo_tactico').filter(
                    id_objetivo_tactico=OuterRef('pk')).annotate(
                    count_id_actividad=Count('id', filter=Q(id_periodo=periodo_actual.id) & Q(id_controlador=controlador.id)))

                count_no_vistos_obj = Ges_Observaciones_sr.objects.values('id_objetivo_tactico').filter(
                    id_objetivo_tactico=OuterRef('pk')).annotate(
                    count_id_actividad=Count('id', filter=Q(observado=1)  & Q(id_controlador=controlador.id) & Q(id_periodo=periodo_actual.id) & (
                       ~Q(user_observa=id_usuario_actual))))

                count_observaciones_obj = Ges_Observaciones_sr.objects.values('id_objetivo_tactico').filter(
                    id_objetivo_tactico=OuterRef('pk')).annotate(
                    count_id_actividad=Count('id', Q(id_periodo=periodo_actual.id)  & Q(id_controlador=controlador.id)))

                replies2 = Ges_Objetivo_Tactico.objects.filter(
                    Q(id_segundo_nivel_id=id_nivel.id_segundo_nivel_id) & Q(id_periodo=periodo_actual.id)).annotate(
                    count_no_vistos=Subquery(count_no_vistos.values('count_id_actividad')),
                    count_actividades=Subquery(count_actividades.values('count_id_actividad')),
                    count_no_vistos_obj=Subquery(count_no_vistos_obj.values('count_id_actividad')),
                    count_observaciones_obj=Subquery(count_observaciones_obj.values('count_id_actividad')),
                    count_observaciones=Subquery(count_observaciones.values('count_id_actividad'))).order_by(
                    '-count_no_vistos', '-count_observaciones')


            if id_orden == 4:
               # replies2 = Ges_Objetivo_Operativo.objects.filter(id_cuarto_nivel_id=id_nivel.id_cuarto_nivel_id)

                count_no_vistos = Ges_Observaciones.objects.values('id_objetivo').filter(Q(
                    id_objetivo=OuterRef('pk')) ).annotate(
                    count_id_actividad=Count('id', filter=Q(observado=1) & Q(id_controlador=controlador.id) & Q(id_periodo=periodo_actual.id) & (~Q(user_observa=id_usuario_actual))))

                count_observaciones = Ges_Observaciones.objects.values('id_objetivo').filter(Q(
                    id_objetivo=OuterRef('pk')) ).annotate(
                    count_id_actividad=Count('id', filter=Q(id_periodo=periodo_actual.id) & Q(id_controlador=controlador.id)))

                count_actividades = Ges_Actividad.objects.values('id_objetivo_operativo').filter(
                    id_objetivo_operativo=OuterRef('pk')).annotate(
                    count_id_actividad=Count('id', filter=Q(id_periodo=periodo_actual.id) & Q(id_controlador=controlador.id)))

                count_no_vistos_obj = Ges_Observaciones_sr.objects.values('id_objetivo_operativo').filter(
                    id_objetivo_operativo=OuterRef('pk')).annotate(
                    count_id_actividad=Count('id', filter=Q(observado=1) & Q(id_controlador=controlador.id) & Q(id_periodo=periodo_actual.id) & (
                        ~Q(user_observa=id_usuario_actual))))

                count_observaciones_obj = Ges_Observaciones_sr.objects.values('id_objetivo_operativo').filter(
                    id_objetivo_operativo=OuterRef('pk')).annotate(
                    count_id_actividad=Count('id', Q(id_periodo=periodo_actual.id) & Q(id_controlador=controlador.id)))

                replies2 = Ges_Objetivo_Operativo.objects.filter(
                    Q(id_cuarto_nivel_id=id_nivel.id_cuarto_nivel_id) & Q(id_periodo=periodo_actual.id)).annotate(
                    count_no_vistos=Subquery(count_no_vistos.values('count_id_actividad')),
                    count_actividades=Subquery(count_actividades.values('count_id_actividad')),
                    count_no_vistos_obj=Subquery(count_no_vistos_obj.values('count_id_actividad')),
                    count_observaciones_obj=Subquery(count_observaciones_obj.values('count_id_actividad')),
                    count_observaciones=Subquery(count_observaciones.values('count_id_actividad'))).order_by(
                    '-count_no_vistos', '-count_observaciones')



            context['orden'] = {'orden_nivel': id_orden}
            context['niveles'] = replies2
            context['objetivo'] = id_nivel
            context['total_disponible'] = {'total_dias': total_dias, 'total_horas': total_horas,
                                       'total_utilizado': total_utilizado,
                                       'consumidas': consumidas,
                                       'avance_porcentaje': avance_porcentaje

                                       }


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
             estado= Glo_Seguimiento.objects.filter(id_periodo=PeriodoActual()).order_by('-id')[0]
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



def ActividadDetalle(request, id):

    template_name = "valida_plan/modal_valida_plan_actividad_detalle.html"
    qs = Ges_Actividad.objects.get(id=id) #Cualquier QS con la que quiera obtener datos para enviar al modal.
    context = {"qs": qs} # aquí le envío lo que quiero al modal para que lo muestre, incluso una lista.


    return render(request, template_name, context)



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
    ahora = datetime.now()
    fecha = ahora.strftime("%d" + " de " + "%B" + " de " + "%Y" + " a las " + "%H:%M")

    try:
        periodo_activo = Glo_Periodos.objects.get(id_estado=1)
    except Glo_Periodos.DoesNotExist:
        return None

    id_usuario_actual = request.user.id  # obtiene id usuario actual
    # try:
    #     usuario_id = Ges_Jefatura.objects.get(id_user=id_usuario_actual)
    # except Ges_Jefatura.DoesNotExist:
    #     usuario_id = None

    try:
        usuario_id = User.objects.get(id=id_usuario_actual)
    except User.DoesNotExist:
        usuario_id = None

    #var = usuario_id.id_nivel.orden_nivel  # Nivel del usuario
    id_controller= request.session['id_controlador_uformula']
    try:
        controlador_id = Ges_Controlador.objects.get(id=id_controller)
    except Ges_Controlador.DoesNotExist:
        controlador_id = 0


    var = controlador_id.nivel_inicial  # Nivel del usuario

    # actualiza el estado a leido
    if var == 2:
        novacio = Ges_Observaciones_sr.objects.filter(
            Q(id_objetivo_tactico=id) & Q(id_periodo=periodo_activo.id) & (~Q(user_observa=id_usuario_actual)))
        if novacio:
            Ges_Observaciones_sr.objects.filter(Q(id_objetivo_tactico=id) & Q(id_periodo=periodo_activo.id) & (
                ~Q(user_observa=id_usuario_actual))).update(
                observado=0,
            )

    if var == 3:
        novacio = Ges_Observaciones_sr.objects.filter(
            Q(id_objetivo_tacticotn=id) & Q(id_periodo=periodo_activo.id) & (~Q(user_observa=id_usuario_actual)))
        if novacio:
            Ges_Observaciones_sr.objects.filter(Q(id_objetivo_tacticotn=id) & Q(id_periodo=periodo_activo.id) & (
                ~Q(user_observa=id_usuario_actual))).update(
                observado=0,
            )
    if var == 4:
        novacio = Ges_Observaciones_sr.objects.filter(
            Q(id_objetivo_operativo=id) & Q(id_periodo=periodo_activo.id) & (~Q(user_observa=id_usuario_actual)))
        if novacio:
            Ges_Observaciones_sr.objects.filter(Q(id_objetivo_operativo=id) & Q(id_periodo=periodo_activo.id) & (
                ~Q(user_observa=id_usuario_actual))).update(
                observado=0,
            )

    if var == 2:
        qs = Ges_Observaciones_sr.objects.filter(Q(id_objetivo_tactico=id) & Q(id_periodo=periodo_activo.id))
    if var == 3:
        qs = Ges_Observaciones_sr.objects.filter(Q(id_objetivo_tacticotn=id) & Q(id_periodo=periodo_activo.id))
    if var == 4:
        qs = Ges_Observaciones_sr.objects.filter(Q(id_objetivo_operativo=id) & Q(id_periodo=periodo_activo.id))

    args = {}

    args['id_objetivo'] = id
    args['estado_plan'] = controlador_id.estado_flujo_id
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


def PeriodoActual():
    try:
        periodo_actual = Glo_Periodos.objects.get(id_estado=1)
    except Glo_Periodos.DoesNotExist:
        return None
    return periodo_actual


