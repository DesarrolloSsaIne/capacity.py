from django.shortcuts import render
from apps.registration.models import logEventos
from django.views.generic import ListView
# Create your views here.
from apps.feriados.models import Ges_Feriados
from apps.jefaturas.models import Ges_Jefatura
from apps.estructura.models import Ges_Niveles
from django.db.models import Q
from django.db.models import Case, CharField, Value, When
from apps.periodos.models import Glo_Periodos
from apps.objetivos.models import Ges_Objetivo_Estrategico, Ges_Objetivo_Operativo, Ges_Objetivo_Tactico, Ges_Objetivo_TacticoTN
from apps.actividades.models import Ges_Actividad
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from apps.actividades.forms import ActividadForm, GestionActividadesUpdateForm
from django.db.models.deletion import ProtectedError
from apps.controlador.models import Ges_Controlador
from apps.gestion_horas.models import Ges_Registro_Horas
from apps.valida_plan2.models import Ges_Observaciones_sr
import datetime
from datetime import date
from django.db.models import Sum
from decimal import *
from apps.valida_plan.models import Ges_Observaciones #apps agregada por JR - sprint 8- Ok
from django.db.models import Subquery, OuterRef, Count,F #import agregado por JR- sprint 8 - Ok
from django.http import JsonResponse

from datetime import datetime, timedelta


def workdays(d, end, excluded=(6, 7)):
    days = []
    while d.date() <= end.date():
        if d.isoweekday() not in excluded:
            days.append(d)
        d += timedelta(days=1)
    return days

class ActividadesObjetivosList(ListView): #clase modificada por JR- sprint 8 - Ok
    model= Ges_Actividad
    template_name = "actividades/actividades_list.html"

    def get_context_data(self,  **kwargs,):
        context = super(ActividadesObjetivosList, self).get_context_data(**kwargs)
        id_usuario_actual= self.request.user.id #obtiene id usuario actual
        id_jefatura = Ges_Jefatura.objects.get(id_user=id_usuario_actual)



        try:
            periodo_actual = Glo_Periodos.objects.get(id_estado=1)
        except Glo_Periodos.DoesNotExist:
            return None

        try:
            id_controlador = Ges_Controlador.objects.get(Q(id_jefatura=id_jefatura) & Q(id_periodo=periodo_actual.id))
        except Ges_Controlador.DoesNotExist:
            id_controlador = 0
            pass

        if id_controlador != 0:
             context['estado_flujo'] = {'estado':id_controlador.estado_flujo}

        if id_controlador == 0:
            context['error'] = {'id': 1}
            return context
            #sys.exit(1)
        else:

            try:
                nivel_usuario= Ges_Jefatura.objects.get(Q(id_user=id_usuario_actual)  & Q(id_periodo=periodo_actual.id))

            except Ges_Jefatura.DoesNotExist:
                context['habilitado'] = {'mensaje': False}
                return None


            try:


                total_dias= list(Ges_Registro_Horas.objects.filter(Q(id_nivel=nivel_usuario.id_nivel.id) & Q(id_periodo=periodo_actual.id)).aggregate(
                    Sum('dias_habiles')).values())[0]

                total_utilizado = list(Ges_Actividad.objects.filter(
                    Q(id_controlador=id_controlador.id) & Q(id_periodo=periodo_actual.id)).aggregate(
                    Sum('total_horas')).values())[0]

                if total_dias != None:
                    total_horas= total_dias * 8
                else:
                    total_horas =0

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

            id_nivel =nivel_usuario.id_nivel.id
            replies = Ges_Niveles.objects.filter(Q(id=id_nivel) & Q(id_periodo=periodo_actual.id)).annotate(
                nivel_order=Case(
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
                    # replies2 = Ges_Objetivo_Tactico.objects.filter(Q(id_segundo_nivel=id_nivel_final) & Q(id_periodo=periodo_actual.id))

                    answer_subquery = Ges_Actividad.objects.values('id_objetivo_tactico_id').filter(
                        id_objetivo_tactico=OuterRef('pk')).annotate(
                        count_actividad=Count('id', filter=Q(id_periodo=periodo_actual.id)))

                    count_no_vistos = Ges_Observaciones.objects.values('id_objetivo').filter(
                        id_objetivo=OuterRef('pk')).annotate(
                        count_id_actividad=Count('id', filter=Q(observado=1) & Q(id_periodo=periodo_actual.id) & (~Q(user_observa = id_usuario_actual)) ))

                    count_observaciones = Ges_Observaciones.objects.values('id_objetivo').filter(
                        id_objetivo=OuterRef('pk')).annotate(
                        count_id_actividad=Count('id'), filter=Q(id_periodo=periodo_actual.id))

                    count_observaciones_obj = Ges_Observaciones_sr.objects.values('id_objetivo_tactico').filter(
                        id_objetivo_tactico=OuterRef('pk')).annotate(
                        count_id_objetivo_tactico=Count('id'), filter=Q(id_periodo=periodo_actual.id))

                    count_no_vistos_obs = Ges_Observaciones_sr.objects.values('id_objetivo_tactico').filter(
                        id_objetivo_tactico=OuterRef('pk')).annotate(
                        count_id_objetivo_tactico=Count('id', filter=Q(observado=1) & Q(id_periodo=periodo_actual.id) & (~Q(user_observa = id_usuario_actual)) ))

                    replies2 = Ges_Objetivo_Tactico.objects.filter(
                        Q(id_segundo_nivel=id_nivel_final) & Q(id_periodo=periodo_actual.id)).annotate(
                        count_no_vistos=Subquery(count_no_vistos.values('count_id_actividad')),
                        count_observaciones=Subquery(count_observaciones.values('count_id_actividad')),
                        count_observaciones_obj=Subquery(count_observaciones_obj.values('count_id_objetivo_tactico')),
                        count_actividad=Subquery(answer_subquery.values('count_actividad')),
                        count_no_vistos_obs=Subquery(count_no_vistos_obs.values('count_id_objetivo_tactico')[0:1])).order_by(
                        '-count_no_vistos',  '-count_observaciones')

                if id_orden == 3:
                    # replies2 = Ges_Objetivo_TacticoTN.objects.filter(Q(id_tercer_nivel=id_nivel_final) & Q(id_periodo=periodo_actual.id))

                    answer_subquery = Ges_Actividad.objects.values('id_objetivo_tacticotn_id').filter(
                        id_objetivo_tacticotn=OuterRef('pk')).annotate(
                        count_actividad=Count('id', filter=Q(id_periodo=periodo_actual.id)))

                    count_no_vistos = Ges_Observaciones.objects.values('id_objetivo').filter(
                        id_objetivo=OuterRef('pk')).annotate(
                        count_id_actividad=Count('id', filter=Q(observado=1) & Q(id_periodo=periodo_actual.id) & (~Q(user_observa = id_usuario_actual)) ))

                    count_observaciones = Ges_Observaciones.objects.values('id_objetivo').filter(
                        id_objetivo=OuterRef('pk')).annotate(
                        count_id_actividad=Count('id'), filter=Q(id_periodo=periodo_actual.id))

                    count_observaciones_obj = Ges_Observaciones_sr.objects.values('id_objetivo_tacticotn').filter(
                        id_objetivo_tacticotn=OuterRef('pk')).annotate(
                        count_id_objetivo_tacticotn=Count('id'), filter=Q(id_periodo=periodo_actual.id))

                    count_no_vistos_obs = Ges_Observaciones_sr.objects.values('id_objetivo_tacticotn').filter(
                        id_objetivo_tacticotn=OuterRef('pk')).annotate(
                        count_id_objetivo_tacticotn=Count('id', filter=Q(observado=1) & Q(id_periodo=periodo_actual.id) & (~Q(user_observa = id_usuario_actual)) ))

                    replies2 = Ges_Objetivo_TacticoTN.objects.filter(
                        Q(id_tercer_nivel=id_nivel_final) & Q(id_periodo=periodo_actual.id)).annotate(
                        count_no_vistos=Subquery(count_no_vistos.values('count_id_actividad')),
                        count_observaciones_obj=Subquery(count_observaciones_obj.values('count_id_objetivo_tacticotn')),
                        count_observaciones=Subquery(count_observaciones.values('count_id_actividad')),
                        count_actividad=Subquery(answer_subquery.values('count_actividad')),
                        count_no_vistos_obs=Subquery(count_no_vistos_obs.values('count_id_objetivo_tacticotn')[0:1])).order_by(
                        '-count_no_vistos', '-count_observaciones')

                if id_orden == 4:
                    # replies2 = Ges_Objetivo_Operativo.objects.filter(Q(id_cuarto_nivel=id_nivel_final) & Q(id_periodo=periodo_actual.id))

                    answer_subquery = Ges_Actividad.objects.values('id_objetivo_operativo_id').filter(
                        id_objetivo_operativo=OuterRef('pk')).annotate(
                        count_id_actividad=Count('id', filter=Q(id_periodo=periodo_actual.id)))

                    count_no_vistos = Ges_Observaciones.objects.values('id_objetivo').filter(
                        id_objetivo=OuterRef('pk')).annotate(
                        count_id_actividad=Count('id', filter=Q(observado=1)  & Q(id_periodo=periodo_actual.id) & (~Q(user_observa = id_usuario_actual)) ))

                    count_observaciones = Ges_Observaciones.objects.values('id_objetivo').filter(
                        id_objetivo=OuterRef('pk')).annotate(
                        count_id_actividad=Count('id'), filter=Q(id_periodo=periodo_actual.id))

                    count_observaciones_obj = Ges_Observaciones_sr.objects.values('id_objetivo_operativo').filter(
                        id_objetivo_operativo=OuterRef('pk')).annotate(
                        count_id_objetivo_operativo=Count('id'), filter=Q(id_periodo=periodo_actual.id))

                    count_no_vistos_obs = Ges_Observaciones_sr.objects.values('id_objetivo_operativo').filter(
                        id_objetivo_operativo=OuterRef('pk')).annotate(
                        count_id_objetivo_operativo=Count('id', filter=Q(observado=1) & Q(id_periodo=periodo_actual.id) & (~Q(user_observa = id_usuario_actual)) ))

                    replies2 = Ges_Objetivo_Operativo.objects.filter(
                        Q(id_cuarto_nivel=id_nivel_final) & Q(id_periodo=periodo_actual.id)).annotate(
                        count_no_vistos=Subquery(count_no_vistos.values('count_id_actividad')),
                        count_observaciones=Subquery(count_observaciones.values('count_id_actividad')),
                        count_observaciones_obj=Subquery(count_observaciones_obj.values('count_id_objetivo_operativo')),
                        count_actividad=Subquery(answer_subquery.values('count_id_actividad')),
                        count_no_vistos_obs=Subquery(count_no_vistos_obs.values('count_id_objetivo_operativo')[0:1])).order_by(
                        '-count_no_vistos',  '-count_observaciones')


            context['niveles'] = replies2

            context['orden'] = {'orden_nivel': id_orden}

            context['total_disponible'] = {'total_dias': total_dias , 'total_horas':total_horas, 'total_utilizado': total_utilizado,
                                           'consumidas': consumidas,
                                           'avance_porcentaje': avance_porcentaje,
                                            'id_jefatura': id_jefatura,
                                           'id_controlador': id_controlador
                                           }

            context['nivel_usuario'] = replies

            self.request.session['id_orden'] = id_orden
            return context



class ActividadesDetail(ListView): #clase modificada por JR- sprint 8 - Ok
    model = Ges_Actividad
    template_name = 'actividades/actividades_detalle.html'

    def get_context_data(self,  **kwargs):
        context = super(ActividadesDetail, self).get_context_data(**kwargs)
        id_usuario_actual = self.request.user.id  # obtiene id usuario actual
        try:
            periodo_actual = Glo_Periodos.objects.get(id_estado=1)
        except Glo_Periodos.DoesNotExist:
            return None
        nombre = ""
        if self.request.session['id_orden']==2:
            #lista_actividades = Ges_Actividad.objects.filter(Q(id_objetivo_tactico=self.kwargs['pk']) & Q(id_periodo=periodo_actual.id))

            count_no_vistos = Ges_Observaciones.objects.values('id_actividad_id').filter(
                id_actividad=OuterRef('pk')).annotate(
                count_id_actividad=Count('id', filter=Q(observado=1)  & Q(id_periodo=periodo_actual.id) & (~Q(user_observa = id_usuario_actual)) ))

            count_observaciones = Ges_Observaciones.objects.values('id_objetivo').filter(
                id_actividad=OuterRef('pk')).annotate(
                count_id_actividad=Count('id'))

            lista_actividades = Ges_Actividad.objects.filter(
                Q(id_objetivo_tactico=self.kwargs['pk']) & Q(id_periodo=periodo_actual.id)).annotate(
                count_no_vistos=Subquery(count_no_vistos.values('count_id_actividad')),
                count_observaciones=Subquery(count_observaciones.values('count_id_actividad')[0:1])).order_by(
                '-count_no_vistos', '-count_observaciones')

            nombre=  Ges_Objetivo_Tactico.objects.get(id=self.kwargs['pk'])
        if self.request.session['id_orden']==3:
           # lista_actividades = Ges_Actividad.objects.filter(Q(id_objetivo_tacticotn=self.kwargs['pk']) & Q(id_periodo=periodo_actual.id))

            count_no_vistos = Ges_Observaciones.objects.values('id_actividad_id').filter(
                id_actividad=OuterRef('pk')).annotate(
                count_id_actividad=Count('id', filter=Q(observado=1)  & Q(id_periodo=periodo_actual.id) & (~Q(user_observa = id_usuario_actual)) ))

            count_observaciones = Ges_Observaciones.objects.values('id_objetivo').filter(
                id_actividad=OuterRef('pk')).annotate(
                count_id_actividad=Count('id'))

            lista_actividades = Ges_Actividad.objects.filter(
                Q(id_objetivo_tacticotn=self.kwargs['pk']) & Q(id_periodo=periodo_actual.id)).annotate(
                count_no_vistos=Subquery(count_no_vistos.values('count_id_actividad')),
                count_observaciones=Subquery(count_observaciones.values('count_id_actividad')[0:1])).order_by(
                '-count_no_vistos', '-count_observaciones')


            nombre = Ges_Objetivo_TacticoTN.objects.get(id=self.kwargs['pk'])
        if self.request.session['id_orden']==4:
            #lista_actividades = Ges_Actividad.objects.filter(Q(id_objetivo_operativo=self.kwargs['pk']) & Q(id_periodo=periodo_actual.id))

            count_no_vistos = Ges_Observaciones.objects.values('id_actividad_id').filter(
                id_actividad=OuterRef('pk')).annotate(
                count_id_actividad=Count('id', filter=Q(observado=1)  & Q(id_periodo=periodo_actual.id) & (~Q(user_observa = id_usuario_actual)) ))

            count_observaciones = Ges_Observaciones.objects.values('id_objetivo').filter(
                id_actividad=OuterRef('pk')).annotate(
                count_id_actividad=Count('id'))

            lista_actividades = Ges_Actividad.objects.filter(
                Q(id_objetivo_operativo=self.kwargs['pk']) & Q(id_periodo=periodo_actual.id)).annotate(
                count_no_vistos=Subquery(count_no_vistos.values('count_id_actividad')),
                count_observaciones=Subquery(count_observaciones.values('count_id_actividad')[0:1])).order_by(
                '-count_no_vistos', '-count_observaciones')


            nombre = Ges_Objetivo_Operativo.objects.get(id=self.kwargs['pk'])

        self.request.session['tv'] = nombre.transversal


        try:
            nivel_usuario = Ges_Jefatura.objects.get(Q(id_user=id_usuario_actual) & Q(id_periodo=periodo_actual.id))
            id_nivel = nivel_usuario.id
        except Ges_Jefatura.DoesNotExist:
            context['habilitado'] = {'mensaje': False}
            return None

        try:
            id_jefatura = Ges_Jefatura.objects.get(id_user=id_usuario_actual)
            id_controlador = Ges_Controlador.objects.get(Q(id_jefatura=id_jefatura) & Q(id_periodo=periodo_actual.id))

            total_dias = list(Ges_Registro_Horas.objects.filter(
                Q(id_nivel=nivel_usuario.id_nivel.id) & Q(id_periodo=periodo_actual.id)).aggregate(
                Sum('dias_habiles')).values())[0]

            total_utilizado = list(Ges_Actividad.objects.filter(
                Q(id_controlador=id_controlador.id) & Q(id_periodo=periodo_actual.id)).aggregate(
                Sum('total_horas')).values())[0]


            if total_dias != None:
                total_horas = total_dias * 8

            else:
                total_horas = 0
            if total_utilizado != None:
                consumidas = total_utilizado
                total_utilizado= total_horas - total_utilizado
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

        context['object_list'] = lista_actividades
        context['nombre_objetivo'] = {'nombre': nombre}
        context['total_disponible'] = {'total_dias': total_dias,
                                       'total_horas': total_horas,
                                       'total_utilizado': total_utilizado,
                                       'consumidas': consumidas,
                                       'avance_porcentaje': avance_porcentaje,
                                       'id_nivel':id_nivel,
                                       'id_controlador':id_controlador}
        self.request.session['id_objetivo']=self.kwargs['pk']
        return context



class ActividadCreate(SuccessMessageMixin, CreateView):
    model = Ges_Actividad
    form_class = ActividadForm
    template_name = 'actividades/actividades_form.html'

    def get_form_kwargs(self, **kwargs):
        kwargs = super(ActividadCreate, self).get_form_kwargs()
        kwargs['transversal'] = self.request.session['tv']

        return kwargs

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)


        id_usuario_actual= self.request.user.id #obtiene id usuario actual

        try:
            periodo_actual = Glo_Periodos.objects.get(id_estado=1)
        except Glo_Periodos.DoesNotExist:
            return None

        try:
            id_jefatura = Ges_Jefatura.objects.get(Q(id_user=id_usuario_actual) & Q(id_periodo=periodo_actual.id))
        except Ges_Jefatura.DoesNotExist:
            return None

        try:
            usuario_controlador = Ges_Controlador.objects.get(id_jefatura=id_jefatura.id)
        except Ges_Controlador.DoesNotExist:
            return None

        fecha_inicio = request.POST['fecha_inicio_actividad']
        fecha_termino = request.POST['fecha_termino_actividad']
        total_horas_post = request.POST['total_horas']



        fecha_inicio_split = datetime.strptime(fecha_inicio, "%Y-%m-%d")
        fecha_termino_split = datetime.strptime(fecha_termino, "%Y-%m-%d")

        anio_inicio = fecha_inicio_split.year
        mes_inicio = fecha_inicio_split.month
        dia_inicio = fecha_inicio_split.day

        anio_termino = fecha_termino_split.year
        mes_termino = fecha_termino_split.month
        dia_termino = fecha_termino_split.day

        dias_habiles_brutos = workdays(datetime(anio_inicio, mes_inicio, dia_inicio),
                                       datetime(anio_termino, mes_termino, dia_termino))

        feriados = Ges_Feriados.objects.filter(Q(id_periodo=periodo_actual.id) & Q(fecha_feriado__range=(
        fecha_inicio, fecha_termino))).count()  # cuenta los feriados entre las fechas de inicio y termino.

        dias_habiles_brutos_feriados = len(dias_habiles_brutos) - feriados
        dias_habiles_brutos_feriados = dias_habiles_brutos_feriados * 8
        dias_habiles_brutos_feriados = int(dias_habiles_brutos_feriados)
        total_horas_post = int(total_horas_post)
        if dias_habiles_brutos_feriados == total_horas_post: # LO MODIFIQUÉ DE == A > EL 01/05 ME FUE IMPOSIBLE AGREGAR UNA ACTIVIDAD CON ESA CONDICION
            if form.is_valid():
                #form.instance.total_horas= 1
                form.instance.estado=1
                form.instance.id_controlador = usuario_controlador
                form.instance.id_periodo = periodo_actual
                if self.request.session['id_orden'] == 2:
                    id_objetivo=Ges_Objetivo_Tactico.objects.get(id=self.request.session['id_objetivo'])
                    form.instance.id_objetivo_tactico= id_objetivo

                if self.request.session['id_orden'] == 3:
                    id_objetivo = Ges_Objetivo_TacticoTN.objects.get(id=self.request.session['id_objetivo'])
                    form.instance.id_objetivo_tacticotn= id_objetivo

                if self.request.session['id_orden'] == 4:
                    id_objetivo = Ges_Objetivo_Operativo.objects.get(id=self.request.session['id_objetivo'])
                    form.instance.id_objetivo_operativo= id_objetivo

                form.save()
                request.session['message_class'] = "alert alert-success"
                messages.success(self.request, "Los datos fueron creados correctamente!")
                return HttpResponseRedirect('/actividades/detalle/' + str(self.request.session['id_objetivo']))
            else:
                request.session['message_class'] = "alert alert-danger"
                messages.error(self.request, "Error interno: No se ha creado el registro. Comuníquese con el administrador.")
                return HttpResponseRedirect('/actividades/detalle/' + str(self.request.session['id_objetivo']))
        else:
            request.session['message_class'] = "alert alert-warning"
            messages.error(self.request,
                           "Aviso :  El total de horas de la actividad supera el total de horas entre la fecha de inicio y término.")
            return HttpResponseRedirect('/actividades/detalle/' + str(self.request.session['id_objetivo']))

class ActividadEdit(SuccessMessageMixin, UpdateView ):
    model = Ges_Actividad
    form_class = GestionActividadesUpdateForm
    template_name = 'actividades/actividades_form_update.html'

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        self.object = self.get_object()
        id_nivel = kwargs['pk']
        instancia_nivel = self.model.objects.get(id=id_nivel)
        form = self.form_class(request.POST, instance=instancia_nivel)
        id_usuario_actual = self.request.user.id  # obtiene id usuario actual

        try:
            periodo_actual = Glo_Periodos.objects.get(id_estado=1)
        except Glo_Periodos.DoesNotExist:
            return None

        try:
            id_jefatura = Ges_Jefatura.objects.get(Q(id_user=id_usuario_actual) & Q(id_periodo=periodo_actual.id))
        except Ges_Jefatura.DoesNotExist:
            return None

        try:
            usuario_controlador = Ges_Controlador.objects.get(id_jefatura=id_jefatura.id)
        except Ges_Controlador.DoesNotExist:
            return None
        fecha_inicio = request.POST['fecha_inicio_actividad']
        fecha_termino = request.POST['fecha_termino_actividad']
        total_horas_post = request.POST['total_horas']

        fecha_inicio_split = datetime.datetime.strptime(fecha_inicio, '%Y-%m-%d')
        fecha_termino_split = datetime.datetime.strptime(fecha_termino, '%Y-%m-%d')

        anio_inicio = fecha_inicio_split.year
        mes_inicio = fecha_inicio_split.month
        dia_inicio = fecha_inicio_split.day

        anio_termino = fecha_termino_split.year
        mes_termino = fecha_termino_split.month
        dia_termino = fecha_termino_split.day

        dias_habiles_brutos = workdays(datetime.datetime(anio_inicio, mes_inicio, dia_inicio),
                                       datetime.datetime(anio_termino, mes_termino, dia_termino))

        feriados = Ges_Feriados.objects.filter(Q(id_periodo=periodo_actual.id) & Q(fecha_feriado__range=(
            fecha_inicio, fecha_termino))).count()  # cuenta los feriados entre las fechas de inicio y termino.

        dias_habiles_brutos_feriados = len(dias_habiles_brutos) - feriados
        dias_habiles_brutos_feriados = dias_habiles_brutos_feriados * 8
        dias_habiles_brutos_feriados = int(dias_habiles_brutos_feriados)
        total_horas_post = int(total_horas_post)
        if dias_habiles_brutos_feriados == total_horas_post:
            if form.is_valid():
                # form.instance.total_horas= 1
                form.instance.estado = 1
                form.instance.id_controlador = usuario_controlador
                form.instance.id_periodo = periodo_actual
                if self.request.session['id_orden'] == 2:
                    id_objetivo = Ges_Objetivo_Tactico.objects.get(id=self.request.session['id_objetivo'])
                    form.instance.id_objetivo_tactico = id_objetivo

                if self.request.session['id_orden'] == 3:
                    id_objetivo = Ges_Objetivo_TacticoTN.objects.get(id=self.request.session['id_objetivo'])
                    form.instance.id_objetivo_tacticotn = id_objetivo

                if self.request.session['id_orden'] == 4:
                    id_objetivo = Ges_Objetivo_Operativo.objects.get(id=self.request.session['id_objetivo'])
                    form.instance.id_objetivo_operativo = id_objetivo

                form.save()
                request.session['message_class'] = "alert alert-success"
                messages.success(self.request, "Los datos fueron actualizados correctamente!")
                return HttpResponseRedirect('/actividades/detalle/' + str(self.request.session['id_objetivo']))
            else:
                request.session['message_class'] = "alert alert-danger"
                messages.error(self.request,
                               "Error interno: No se ha creado el registro. Comuníquese con el administrador.")
                return HttpResponseRedirect('/actividades/detalle/' + str(self.request.session['id_objetivo']))
        else:
            request.session['message_class'] = "alert alert-warning"
            messages.error(self.request,
                           "Aviso :  El total de horas de la actividad supera el total de horas entre la fecha de inicio y término.")
            return HttpResponseRedirect('/actividades/detalle/' + str(self.request.session['id_objetivo']))




class ActividadesDelete(SuccessMessageMixin, DeleteView ):
    model = Ges_Actividad

    template_name = 'actividades/actividades_delete.html'

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        try:
            obj.delete()
            request.session['message_class'] = "alert alert-success"
            messages.success(self.request, "El registro fue eliminado correctamente!")
            return HttpResponseRedirect('/actividades/detalle/' + str(self.request.session['id_objetivo']))

        except ProtectedError as e:
            request.session['message_class'] = "alert alert-danger"
            messages.error(request, "Error de integridad: Este nivel posee subniveles los que deben ser borrados antes de borrar este nivel.")
            return HttpResponseRedirect('/actividades/detalle/' + str(self.request.session['id_objetivo']))

        except Exception  as e:
            request.session['message_class'] = "alert alert-danger"
            messages.error(request, "Error interno: No se ha eliminado el registro. Comuníquese con el administrador.")
            return HttpResponseRedirect('/actividades/detalle/' + str(self.request.session['id_objetivo']))




def GestionObservacionesObjetivos(request, id):
    template_name = "actividades/modal_observaciones_objetivos.html"
    response_data = {}
    ahora = datetime.now()
    fecha = ahora.strftime("%d" + " de " + "%B" + " de " + "%Y" + " a las " + "%H:%M")

    try:
        periodo_activo = Glo_Periodos.objects.get(id_estado=1)
    except Glo_Periodos.DoesNotExist:
        return None

    id_usuario_actual = request.user.id  # obtiene id usuario actual
    try:
        usuario_id = Ges_Jefatura.objects.get(id_user=id_usuario_actual)
    except Ges_Jefatura.DoesNotExist:
        usuario_id = None

    var= usuario_id.id_nivel.orden_nivel # Nivel del usuario

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

        try:
            controlador_id = Ges_Controlador.objects.get(id_jefatura=usuario_id.id)
        except Ges_Controlador.DoesNotExist:
            controlador_id = 0


        if controlador_id == 0:
            controlador = 0
        else:
            controlador = controlador_id.id

        observacion = request.POST.get('observacion')

        response_data['observacion'] = observacion
        response_data['id_actividad'] = id
        response_data['fecha'] = fecha

        if var == 2:
            Ges_Observaciones_sr.objects.create(
                observacion=observacion, id_controlador=controlador, user_observa=usuario_id.id_user,
                id_objetivo_tactico_id=id, id_periodo_id=periodo_activo.id, observado=1,
            )
        if var == 3:
            Ges_Observaciones_sr.objects.create(
                observacion=observacion, id_controlador=controlador, user_observa=usuario_id.id_user,
                id_objetivo_tacticotn_id=id, id_periodo_id=periodo_activo.id, observado=1,
            )
        if var == 4:
            Ges_Observaciones_sr.objects.create(
                observacion=observacion, id_controlador=controlador, user_observa=usuario_id.id_user,
                id_objetivo_operativo_id=id, id_periodo_id=periodo_activo.id, observado=1,
            )



        return JsonResponse(response_data)

    return render(request, template_name, args)



def GestionObservacionesActividades(request, id):
    template_name = "actividades/modal_observaciones_actividades.html"
    response_data = {}
    ahora = datetime.now()
    fecha = ahora.strftime("%d" + " de " + "%B" + " de " + "%Y" + " a las " + "%H:%M")

    try:
        periodo_activo = Glo_Periodos.objects.get(id_estado=1)
    except Glo_Periodos.DoesNotExist:
        return None

    id_usuario_actual = request.user.id  # obtiene id usuario actual
    try:
        usuario_id = Ges_Jefatura.objects.get(id_user=id_usuario_actual)
    except Ges_Jefatura.DoesNotExist:
        usuario_id = None

    try:
        controlador_id = Ges_Controlador.objects.get(id_jefatura=usuario_id.id)
    except Ges_Controlador.DoesNotExist:
        controlador_id = 0

    if controlador_id == 0:
        controlador = 0
    else:
        controlador = controlador_id.id

    try:
        actividad = Ges_Actividad.objects.get(id=id)
    except Ges_Actividad.DoesNotExist:
        actividad = 0



    var = usuario_id.id_nivel.orden_nivel  # Nivel del usuario

    if var==2:
        id_objetivo= actividad.id_objetivo_tactico_id
    if var==3:
        id_objetivo = actividad.id_objetivo_tacticotn_id
    if var==4:
        id_objetivo = actividad.id_objetivo_operativo_id

    #actualiza el estado a leido
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
            observacion = observacion, id_controlador=controlador, user_observa= usuario_id.id_user, id_actividad_id=id, id_periodo_id=periodo_activo.id,
           id_objetivo=id_objetivo, observado=1,

            )

        return JsonResponse(response_data)

    return render(request, template_name, args)





def update_estate(request):
    if request.POST.get('action') == 'post':
        try:
            periodo_actual = Glo_Periodos.objects.get(id_estado=1)
        except Glo_Periodos.DoesNotExist:
            return None
        try:
            id = request.POST.get('id')
            controlador = Ges_Controlador.objects.get(Q(id_jefatura=id) & Q(id_periodo=periodo_actual.id))
            estado = 3
            controlador.estado_flujo_id = int(estado)
            tipo_evento = "Inicio Formulación"
            metodo = "Actividades - Update_estate"
            usuario_evento = controlador.id_jefatura.id_user
            jefatura_dirigida = None
            logEventosCreate(tipo_evento, metodo, usuario_evento, jefatura_dirigida)
            controlador.save()
            request.session['message_class'] = "alert alert-success"
            #messages.success(request, "El registro fue eliminado correctamente!")
            return render(request, '/actividades/listar/', {'messages':'success'})
            #return HttpResponseRedirect('/actividades/listar/')
        except Exception  as e:
            messages.error(request, "Error interno: No se ha actualizado el registro. Comuníquese con el administrador.")
            return HttpResponseRedirect('/actividades/listar/')



def logEventosCreate(tipo_evento, metodo ,usuario_evento, jefatura_dirigida):
    logEventos.objects.create(
        tipo_evento=tipo_evento,
        metodo=metodo,
        usuario_evento=usuario_evento,
        jefatura_dirigida=jefatura_dirigida,
    )
    return None



