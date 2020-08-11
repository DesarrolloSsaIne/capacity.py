from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from apps.estructura.models import Ges_Niveles
from apps.jefaturas.models import Ges_Jefatura
from apps.controlador.models import Ges_Controlador
from django.db.models import Q
from apps.periodos.models import Glo_Periodos
from apps.actividades.models import Ges_Actividad
from apps.objetivos.models import  Ges_Objetivo_Operativo, Ges_Objetivo_Tactico, Ges_Objetivo_TacticoTN
from apps.valida_plan2.forms import   PlanUpdateForm
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from apps.valida_plan2.models import Ges_Observaciones_sr
from apps.valida_plan.models import Ges_Observaciones
from django.db.models import Subquery, OuterRef, Count # import agregados por JR - sprint 8 - ok
from django.db.models.deletion import ProtectedError
from django.urls import reverse_lazy
from django.http import JsonResponse

from django.core import mail
from django.conf import settings
from django.utils.module_loading import import_string
from django.core.mail import EmailMultiAlternatives
from django.db.models.deletion import ProtectedError
from apps.eje.models import Ges_Ejes
from datetime import datetime
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



def EnviarCorreoRechazo_jefaturas(emails_jefaturas, area_plan):
    # try:
    #     periodo_actual = Glo_Periodos.objects.get(id_estado=1)
    # except Glo_Periodos.DoesNotExist:
    #     return None

    ahora = datetime.now()
    fecha = ahora.strftime("%d" + "/" + "%m" + "/" + "%Y" + " a las " + "%H:%M")

    #controladorPlan = Ges_Jefatura.objects.values_list('id_user__email' , flat=True).filter(Q(id_periodo=periodo_actual) & Q(id=id_jefatura))
    idcorreoJefatura=emails_jefaturas
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
    messageHtml = 'Estimada(o) Usuaria(o),<br> Se informa que con fecha <b>'+ fecha +'</b> el plan de gestión fue aprobado y enviado al área de Planificación para su revisión final. <br> Atte. <br>Subdpto. de Planificación Institucional.<br><p style="font-size:12px;color:red;">correo generado automaticamente favor no responder.'

    email = EmailMessage(subject, messageHtml ,to=idcorreoJefatura)

    email.content_subtype='html'
    email.send()



def EnviarCorreoAcepta_jefaturas(emails_jefaturas, area_plan):
    # try:
    #     periodo_actual = Glo_Periodos.objects.get(id_estado=1)
    # except Glo_Periodos.DoesNotExist:
    #     return None

    ahora = datetime.now()
    fecha = ahora.strftime("%d" + "/" + "%m" + "/" + "%Y" + " a las " + "%H:%M")

    #controladorPlan = Ges_Jefatura.objects.values_list('id_user__email' , flat=True).filter(Q(id_periodo=periodo_actual) & Q(id=id_jefatura))
    idcorreoJefatura=emails_jefaturas
    area_plan=str(area_plan)

    subject = 'Aprobación Plan de Gestión '
    messageHtml = 'Estimada(o) Usuaria(o),<br> Se informa que con fecha <b>'+ fecha +'</b> el plan de gestión correspondiente a <b>' + area_plan + '</b> fue aprobado y enviado al área de Planificación para su revisión final . <br> Atte. <br>Subdpto. de Planificación Institucional.<br><p style="font-size:12px;color:red;">correo generado automaticamente favor no responder.'

    email = EmailMessage(subject, messageHtml ,to=idcorreoJefatura)

    email.content_subtype='html'
    email.send()

def EnviarCorreoAcepta_Planificacion(email_planificacion, area_plan):
    # try:
    #     periodo_actual = Glo_Periodos.objects.get(id_estado=1)
    # except Glo_Periodos.DoesNotExist:
    #     return None

    ahora = datetime.now()
    fecha = ahora.strftime("%d" + "/" + "%m" + "/" + "%Y" + " a las " + "%H:%M")

    #controladorPlan = Ges_Jefatura.objects.values_list('id_user__email' , flat=True).filter(Q(id_periodo=periodo_actual) & Q(id=id_jefatura))
    idcorreoJefatura=[str(email_planificacion)]
    area_plan=str(area_plan)

    subject = 'Aprobación Plan de Gestión '
    messageHtml = 'Estimada(o) Usuaria(o),<br> Se informa que con fecha <b>'+ fecha +'</b> el plan de gestión correspondiente a <b>' + area_plan + '</b> fue aprobado y enviado a su bandeja para ser derivado a un Analista. <br> Atte. <br>Subdpto. de Planificación Institucional.<br><p style="font-size:12px;color:red;">correo generado automaticamente favor no responder.'

    email = EmailMessage(subject, messageHtml ,to=idcorreoJefatura)

    email.content_subtype='html'
    email.send()



class RechazaPlan(UpdateView):
    model = Ges_Controlador
    form_class = PlanUpdateForm
    template_name = 'valida_plan2/valida_plan_rechaza_form.html'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        id_controlador = kwargs['pk']
        id_usuario_actual = self.request.user.id  # obtiene id usuario actual
        try:
            id_jefatura = Ges_Jefatura.objects.get(id_user=id_usuario_actual)
        except Ges_Jefatura.DoesNotExist:
            return None
        try:
            periodo_actual = Glo_Periodos.objects.get(id_estado=1)
        except Glo_Periodos.DoesNotExist:
            return None

        controladorPlan = self.model.objects.get(Q(id=id_controlador) & Q(id_periodo=periodo_actual.id))
        email_jefatura = controladorPlan.id_jefatura.id_user.email    #correo de rechazo
        email_primera_jefatura= controladorPlan.jefatura_primerarevision.id_user.email
        email_segunda_jefatura= self.request.user.email

        area_plan = controladorPlan.id_jefatura.id_nivel
        emails_jefaturas=[email_primera_jefatura,email_segunda_jefatura]

        lista_observaciones = Ges_Observaciones_sr.objects.filter(Q(id_controlador=id_controlador) & Q(id_periodo=periodo_actual.id)
                                                         & Q(observado=1) & Q(user_observa=id_usuario_actual)).count()

        estado = 9 # estado rechazo segundo nivel
        controladorPlan.estado_flujo_id = int(estado)
        if int(lista_observaciones) > 0:
            try:
                controladorPlan.save()
                try:

                    EnviarCorreoRechazo_formulador(email_jefatura)
                    EnviarCorreoRechazo_jefaturas(emails_jefaturas,area_plan )

                    request.session['message_class'] = "alert alert-success"  # Tipo mensaje
                    messages.success(request,
                                     "El Plan fue rechazado correctamente y el correo de notificación fue enviado a quien formuló el plan!.")  # mensaje
                    return HttpResponseRedirect('/valida_plan2/listarUnidades2')  # Redirije a la pantalla principal

                except:

                    request.session['message_class'] = "alert alert-warning"  # Tipo mensaje
                    messages.success(request,
                                     "El Plan fue rechazado correctamente!, pero el servicio de correo tuvo un inconveniente favor comuníquese con su la jefatura que redactó el plan para informarle del rechazo.")  # mensaje
                    return HttpResponseRedirect('/valida_plan2/listarUnidades2')  # Redirije a la pantalla principal


            except:
                request.session['message_class'] = "alert alert-danger"
                messages.error(self.request,
                               "Error interno: El plan no fue rechazado, intente nuevamente o comuníquese con el administrador.")
                return HttpResponseRedirect('/valida_plan2/listarUnidades2')
        else:
            request.session['message_class'] = "alert alert-danger"
            messages.error(self.request, "Debe ingresar al menos una observacion para rechazar el plan.")
            return HttpResponseRedirect('/valida_plan2/listarUnidades2')


class AceptaPlan(UpdateView):
    model = Ges_Controlador
    form_class = PlanUpdateForm
    template_name = 'valida_plan2/valida_plan_acepta_form.html'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        id_controlador = kwargs['pk']

        try:
            periodo_actual = Glo_Periodos.objects.get(id_estado=1)
        except Glo_Periodos.DoesNotExist:
            return None

        controladorPlan = self.model.objects.get(Q(id=id_controlador) & Q(id_periodo=periodo_actual.id))

        email_jefatura = controladorPlan.id_jefatura.id_user.email    #correo de rechazo
        email_primera_jefatura= controladorPlan.jefatura_primerarevision.id_user.email
        email_segunda_jefatura= self.request.user.email
        email_admin_planificacion = settings.EMAIL_HOST_USER
        area_plan = controladorPlan.id_jefatura.id_nivel
        emails_jefaturas=[email_primera_jefatura,email_segunda_jefatura]

        existeAnalista = controladorPlan.analista_asignado
        estado = 0
        if existeAnalista:
            estado = 6
        else:
            estado = 10
        estado = int(estado)
        controladorPlan.estado_flujo_id = int(estado)
        try:
            controladorPlan.save()

            try:

                EnviarCorreoAcepta_formulador(email_jefatura)
                EnviarCorreoAcepta_jefaturas(emails_jefaturas, area_plan)
                EnviarCorreoAcepta_Planificacion(email_admin_planificacion,area_plan )

                request.session['message_class'] = "alert alert-success"  # Tipo mensaje
                messages.success(request,
                                 "El Plan fue aceptado correctamente y el correo de notificación fue enviado al área de Planificación!.")  # mensaje
                return HttpResponseRedirect('/valida_plan2/listarUnidades2')  # Redirije a la pantalla principal

            except:

                request.session['message_class'] = "alert alert-warning"  # Tipo mensaje
                messages.success(request,
                                 "El Plan fue aceptado correctamente!, pero el servicio de correo tuvo un inconveniente favor comuníquese con el área de Planificación informando el envío del plan de gestión.")  # mensaje
                return HttpResponseRedirect('/valida_plan2/listarUnidades2')  # Redirije a la pantalla principal

            # request.session['message_class'] = "alert alert-success"
            # messages.success(self.request, "El plan fue aceptado correctamente y enviado al área de Planificación para su revisión.")
            # #idcorreoJefatura = [email_jefatura_ingresaAct]
            # subject = 'Plan Aceptado'
            # message = 'Estimada(o) Usuaria(o), Su plan enviado para revisión fue aceptado.  Atte. Subdpto. de Planificación Institucional.>Correo generado automaticamente no responder.'
            # messageHtml = 'Estimada(o) Usuaria(o),<br> Su plan enviado para revisión fue aceptado. <br> Atte. <br>Subdpto. de Planificación Institucional.<br><p style="font-size:12px;color:red;">correo generado automaticamente favor no responder.'
            # # send_correo(idcorreoJefatura, subject, message, messageHtml)
            # # este correo se le debe enviar al analista
            # #email_jefatura_2revision = email_jefatura_2revision
            # #idcorreoJefatura = [email_jefatura_2revision]
            # subject = 'Revisión de Plan'
            # message = 'Estimada(o) Usuaria(o), Se ha cargado un nuevo plan  para su revisión.  Atte. Subdpto. de Planificación Institucional.>Correo generado automaticamente no responder.'
            # messageHtml = 'Estimada(o) Usuaria(o),<br> Se ha cargado un nuevo plan  para su revisión. <br> Atte. <br>Subdpto. de Planificación Institucional.<br><p style="font-size:12px;color:red;">correo generado automaticamente favor no responder.'
            # # send_correo(idcorreoJefatura, subject, message, messageHtml)
            # return HttpResponseRedirect('/valida_plan2/listarUnidades2')
        except:
            request.session['message_class'] = "alert alert-danger"
            messages.error(self.request,
                           "Error interno: El plan no ha podido ser aceptado. Comuníquese con el administrador.")
            return HttpResponseRedirect('/valida_plan2/listarUnidades2')






#######################################################################################################################
#######################################################################################################################
#######################################################################################################################


class UnidadesList(ListView): #Modificado por JR- sprint 8 - OK
    model = Ges_Niveles
    template_name = 'valida_plan2/valida_plan_list.html'

    def get_context_data(self, **kwargs):
        context = super(UnidadesList, self).get_context_data(**kwargs)
        id_usuario_actual = self.request.user.id  # obtiene id usuario actual

        try:
            periodo_actual = Glo_Periodos.objects.get(id_estado=1)
        except Glo_Periodos.DoesNotExist:
            return None

        try:
            id_jefatura = Ges_Jefatura.objects.get(id_user=id_usuario_actual)

            count_no_vistos = Ges_Observaciones_sr.objects.values('id_controlador').filter(
                id_controlador=OuterRef('pk')).annotate(
                count_id_actividad=Count('id', filter=Q(observado=1)  & Q(id_periodo=periodo_actual.id) & (~Q(user_observa=id_usuario_actual))))

            count_observaciones = Ges_Observaciones_sr.objects.values('id_controlador').filter(
                id_controlador=OuterRef('pk')).annotate(
                count_id_actividad=Count('id'))

            id_controlador = Ges_Controlador.objects.filter(
                Q(jefatura_segundarevision=id_jefatura.id) & Q(id_periodo=periodo_actual.id) & Q(estado_flujo=5)).annotate(
                count_no_vistos=Subquery(count_no_vistos.values('count_id_actividad')),
                count_observaciones=Subquery(count_observaciones.values('count_id_actividad'))).order_by(
                '-count_no_vistos', '-count_observaciones')

            id_jefatura = Ges_Jefatura.objects.filter(id_user=id_usuario_actual)

            context['object_list'] = id_controlador
            context['object_list3'] = id_jefatura

            return context

        except Ges_Jefatura.DoesNotExist:
            context['habilitado'] = {'mensaje': False}
            return None

class Objetivos(ListView): #Modificado por JR- sprint 8 - OK
    model = Ges_Actividad
    template_name = 'valida_plan2/valida_plan_detalle.html'

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
                answer_subquery = Ges_Actividad.objects.values('id_objetivo_tacticotn_id').filter(
                   id_objetivo_tacticotn=OuterRef('pk')).annotate(
                   count_actividad=Count('id', filter=Q(id_periodo=periodo_actual.id)))

                count_no_vistos = Ges_Observaciones_sr.objects.values('id_objetivo_tacticotn').filter(
                    id_objetivo_tacticotn=OuterRef('pk')).annotate(
                    count_id_actividad=Count('id', filter=Q(observado=1) & Q(id_periodo=periodo_actual.id) & (~Q(user_observa=id_usuario_actual))))

                count_observaciones = Ges_Observaciones_sr.objects.values('id_objetivo_tacticotn').filter(
                    id_objetivo_tacticotn=OuterRef('pk')).annotate(
                    count_id_actividad=Count('id'))

                replies2 = Ges_Objetivo_TacticoTN.objects.filter(
                    Q(id_tercer_nivel_id=id_nivel.id_tercer_nivel_id) & Q(id_periodo=periodo_actual.id)).annotate(
                    count_no_vistos=Subquery(count_no_vistos.values('count_id_actividad')),
                    count_observaciones=Subquery(count_observaciones.values('count_id_actividad')),
                    count_actividad=Subquery(answer_subquery.values('count_actividad')[0:1])).order_by(
                    '-count_no_vistos', '-count_observaciones')


            if id_orden == 2:
               # replies2 = Ges_Objetivo_Tactico.objects.filter(id_segundo_nivel_id=id_nivel.id_segundo_nivel_id)

                answer_subquery = Ges_Actividad.objects.values('id_objetivo_tactico_id').filter(
                   id_objetivo_tactico=OuterRef('pk')).annotate(
                   count_actividad=Count('id', filter=Q(id_periodo=periodo_actual.id)))

                count_no_vistos = Ges_Observaciones_sr.objects.values('id_objetivo_tactico').filter(
                    id_objetivo_tactico=OuterRef('pk')).annotate(
                    count_id_actividad=Count('id', filter=Q(observado=1) & Q(id_periodo=periodo_actual.id) & (~Q(user_observa=id_usuario_actual))))

                count_observaciones = Ges_Observaciones_sr.objects.values('id_objetivo_tactico').filter(
                    id_objetivo_tactico=OuterRef('pk')).annotate(
                    count_id_actividad=Count('id'))

                replies2 = Ges_Objetivo_Tactico.objects.filter(
                    Q(id_segundo_nivel_id=id_nivel.id_segundo_nivel_id) & Q(id_periodo=periodo_actual.id)).annotate(
                    count_no_vistos=Subquery(count_no_vistos.values('count_id_actividad')),
                    count_observaciones=Subquery(count_observaciones.values('count_id_actividad')),
                    count_actividad=Subquery(answer_subquery.values('count_actividad')[0:1])).order_by(
                    '-count_no_vistos', '-count_observaciones')


            if id_orden == 4:
               # replies2 = Ges_Objetivo_Operativo.objects.filter(id_cuarto_nivel_id=id_nivel.id_cuarto_nivel_id)

                answer_subquery = Ges_Actividad.objects.values('id_objetivo_operativo').filter(
                   id_objetivo_operativo=OuterRef('pk')).annotate(
                   count_id_actividad=Count('id', filter=Q(id_periodo=periodo_actual.id)))

                count_no_vistos = Ges_Observaciones_sr.objects.values('id_objetivo_operativo').filter(
                    id_objetivo_operativo=OuterRef('pk')).annotate(
                    count_id_actividad=Count('id', filter=Q(observado=1) & Q(id_periodo=periodo_actual.id) & (~Q(user_observa=id_usuario_actual))))

                count_observaciones = Ges_Observaciones_sr.objects.values('id_objetivo_operativo').filter(
                    id_objetivo_operativo=OuterRef('pk')).annotate(
                    count_id_actividad=Count('id'))

                replies2 = Ges_Objetivo_Operativo.objects.filter(
                    Q(id_cuarto_nivel_id=id_nivel.id_cuarto_nivel_id) & Q(id_periodo=periodo_actual.id)).annotate(
                    count_no_vistos=Subquery(count_no_vistos.values('count_id_actividad')),
                    count_observaciones=Subquery(count_observaciones.values('count_id_actividad')),
                    count_actividad=Subquery(answer_subquery.values('count_id_actividad'))
                    ).order_by(
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
    template_name = 'valida_plan2/valida_plan_list_actividades.html'

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

            count_observaciones = Ges_Observaciones_sr.objects.values('id_actividad').filter(id_actividad=OuterRef('pk')).annotate(
            count_id_actividad=Count('id'))

            lista_actividades = Ges_Actividad.objects.filter(
              Q(id_objetivo_tactico=self.kwargs['pk']) & Q(id_periodo=periodo_actual.id)).annotate(
             count_observaciones=Subquery(count_observaciones.values('count_id_actividad'))).order_by('-count_observaciones')

            nombre=  Ges_Objetivo_Tactico.objects.get(id=self.kwargs['pk'])

        if self.request.session['id_orden']==3:
           # lista_actividades = Ges_Actividad.objects.filter(Q(id_objetivo_tacticotn=self.kwargs['pk']) & Q(id_periodo=periodo_actual.id))


            count_observaciones = Ges_Observaciones.objects.values('id_actividad').filter(id_actividad=OuterRef('pk')).annotate(
            count_id_actividad=Count('id'))

            lista_actividades = Ges_Actividad.objects.filter(
              Q(id_objetivo_tacticotn=self.kwargs['pk']) & Q(id_periodo=periodo_actual.id)).annotate(
             count_observaciones=Subquery(count_observaciones.values('count_id_actividad'))).order_by('-count_observaciones')


            nombre = Ges_Objetivo_TacticoTN.objects.get(id=self.kwargs['pk'])

        if self.request.session['id_orden']==4:


            count_observaciones = Ges_Observaciones.objects.values('id_actividad').filter(id_actividad=OuterRef('pk')).annotate(
            count_id_actividad=Count('id'))

            lista_actividades = Ges_Actividad.objects.filter(
              Q(id_objetivo_operativo=self.kwargs['pk']) & Q(id_periodo=periodo_actual.id)).annotate(
             count_observaciones=Subquery(count_observaciones.values('count_id_actividad'))).order_by('-count_observaciones')


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


        return context

class ObservacionesListar(ListView): #Modificado por JR- sprint 8 - OK
    model = Ges_Observaciones_sr
    template_name = 'valida_plan2/valida_plan_observaciones_list.html'


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

        lista_observaciones = Ges_Observaciones_sr.objects.filter(Q(id_periodo=periodo_actual.id) & Q(id_actividad=id_actividad)).order_by('-fecha_registro')
        context['object_list'] = lista_observaciones

        context['id_actividad'] = {'id': id_objetivo}
        context['User'] = {'id': id_usuario_actual}
        context['actividad'] = {'descripcion_actividad': actividad.descripcion_actividad}

        return context

def GestionObservacionesVer(request, id):
    template_name = "valida_plan2/modal_observaciones_view.html"
    response_data = {}


    try:
        periodo_activo = Glo_Periodos.objects.get(id_estado=1)
    except Glo_Periodos.DoesNotExist:
        return None



    qs = Ges_Observaciones.objects.filter(Q(id_actividad=id) & Q(id_periodo=periodo_activo.id))

    args = {}

    args['id_actividad'] = id
    args['object_list']= qs



    if request.POST.get('action') == 'post':


       # observacion = request.POST.get('observacion')


        return JsonResponse(response_data)

    return render(request, template_name, args)

def GestionObservacionesObjetivosVp2(request, id):
    template_name = "valida_plan2/modal_observaciones_objetivos_vp2.html"
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
        usuario_id = Ges_Jefatura.objects.get(id_user=id_usuario_actual)
    except Ges_Jefatura.DoesNotExist:
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
                observacion=observacion, id_controlador=id_controller, user_observa=usuario_id.id_user,
                id_objetivo_tactico_id=id, id_periodo_id=periodo_activo.id, observado=1,
            )
        if var == 3:
            Ges_Observaciones_sr.objects.create(
                observacion=observacion, id_controlador=id_controller, user_observa=usuario_id.id_user,
                id_objetivo_tacticotn_id=id, id_periodo_id=periodo_activo.id, observado=1,
            )
        if var == 4:
            Ges_Observaciones_sr.objects.create(
                observacion=observacion, id_controlador=id_controller, user_observa=usuario_id.id_user,
                id_objetivo_operativo_id=id, id_periodo_id=periodo_activo.id, observado=1,
            )



        return JsonResponse(response_data)

    return render(request, template_name, args)

