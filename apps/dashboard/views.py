from django.shortcuts import render
from django.contrib.auth.models import User, Group
from apps.controlador.models import Ges_Controlador
from apps.actividades.models import Ges_Actividad
from apps.periodos.models import Glo_Seguimiento, Glo_validacion

from apps.jefaturas.models import Ges_Jefatura
from django.db.models import Subquery, OuterRef, Count, Max, Sum
from django.db.models import QuerySet
from django.db.models import Q
from apps.objetivos.models import Ges_Objetivo_Estrategico, Ges_Objetivo_Operativo, Ges_Objetivo_Tactico, Ges_Objetivo_TacticoTN
from apps.estructura.models import Ges_CuartoNivel, Ges_SegundoNivel, Ges_TercerNivel
from apps.periodos.models import Glo_Periodos
from django.views.generic import TemplateView
from django.contrib.auth.models import User
from django.db import models
import csv
import xlwt
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.db.models.functions import TruncMonth
from django.db.models import Count
from django.views.defaults import page_not_found
import datetime
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


# Dirije al dashboard al momento del login además agrega la variable se sesión grupo #
#


class InicioDashboard(TemplateView):
    #template_name = 'dashboard/dashboard.html'    EL TEMPLATE ESTÁ EN EL METODO GET AL FINAL DE LA CLASE


    def get_context_data(self, **kwargs):


        context = super(InicioDashboard, self).get_context_data(**kwargs)

        id_usuario_actual = self.request.user.id  # obtiene id usuario actual


        Grupo = Group.objects.get(user=self.request.user)

        self.request.session['grupo'] = str(Grupo)

        try:
            periodo_actual = Glo_Periodos.objects.get(id_estado=1)
        except Glo_Periodos.DoesNotExist:
            return None



        if Grupo.id==2 or Grupo.id==5 or Grupo.id==6:

            try:
                estado_seguimiento = Glo_Seguimiento.objects.order_by('-id')[0]
            except IndexError:
                estado_seguimiento = 0
                pass

            if estado_seguimiento != 0:
                context['estado_seguimiento'] = {'estado': estado_seguimiento.id_estado_seguimiento}
            else:
                context['estado_seguimiento'] = {'estado': '-'}

            try:
                estado_validacion = Glo_validacion.objects.order_by('-id')[0]
            except IndexError:
                estado_validacion = 0
                pass

            if estado_validacion != 0:
                context['estado_validacion'] = {'estado': estado_validacion.id_estado_periodo}
            else:
                context['estado_validacion'] = {'estado': '-'}


            total_actividades_institucion = list(
                Ges_Actividad.objects.filter( Q(id_periodo=periodo_actual)).aggregate(
                    Count('id')).values())[0]

            context['total_actividades_institucion'] = {'cantidad': total_actividades_institucion}

            # Si piden los estados de los planes en dashboard
            # PlanesPorArea = Ges_Actividad.objects.filter(
            #     Q(id_periodo=periodo_actual) ).values(
            #     'id_controlador__id_jefatura__id_nivel__descripcion_nivel',
            #     'id_controlador__estado_flujo__descripcion_estado').annotate(
            #     CantidadPlan=Count('id'))
            #
            # context["PlanesPorArea"] = PlanesPorArea


            ps = Ges_Actividad.objects.filter(id_periodo=periodo_actual).values('id_estado_actividad__descripcion_estado').annotate(CantidadEst=Count('id')).order_by('id_estado_actividad__orden') # estado por jefatura
            ps2 = Ges_Controlador.objects.filter(id_periodo=periodo_actual).values('estado_flujo__descripcion_estado').annotate(CantidadAct=Count('id'))# Cantidad act. por areas


            UnidadesAsociadas = Ges_Actividad.objects.filter(
                Q(id_periodo=periodo_actual)).values(
                'id_controlador__id_jefatura__id_nivel__descripcion_nivel').annotate(
                CantidadPlan=Count('id')).order_by(
                'id_controlador')

            controladores = list(Ges_Actividad.objects.filter(
                Q(id_periodo=periodo_actual)).values_list(
                'id_controlador', flat=True).distinct().order_by(
                'id_controlador'))  ##Trae solo los controladores que han ingresado una actividad

            # controladores = list(Ges_Controlador.objects.filter(Q(id_periodo=periodo_actual)).values_list('id', flat=True).order_by(
            #     'id')) ##Trae todos los controladores sin importar sin ingresaron algo

            ValFinalizadas = []
            ValEnCurso = []
            ValNoIniciado = []
            ValConRetraso = []
            ValSinMovimiento = []
            ValEliminadas = []

            for i in controladores:
                val = Ges_Actividad.objects.filter(
                    Q(id_controlador=i) & Q(id_periodo=periodo_actual) & Q(id_estado_actividad=7)).count()
                ValFinalizadas.append(val)

                val = Ges_Actividad.objects.filter(
                    Q(id_controlador=i) & Q(id_periodo=periodo_actual) & (Q(id_estado_actividad=3) | Q(id_estado_actividad=8))).count()
                ValEnCurso.append(val)

                val = Ges_Actividad.objects.filter(
                    Q(id_controlador=i) & Q(id_periodo=periodo_actual) & Q(id_estado_actividad=4)).count()
                ValNoIniciado.append(val)

                val = Ges_Actividad.objects.filter(
                    Q(id_controlador=i) & Q(id_periodo=periodo_actual) & (Q(id_estado_actividad=1) | Q(id_estado_actividad=2))).count()
                ValConRetraso.append(val)

                val = Ges_Actividad.objects.filter(
                    Q(id_controlador=i) & Q(id_periodo=periodo_actual) & (Q(id_estado_actividad=5) | Q(id_estado_actividad=6))).count()
                ValSinMovimiento.append(val)

                val = Ges_Actividad.objects.filter(
                    Q(id_controlador=i) & Q(id_periodo=periodo_actual) & (Q(id_estado_actividad=9) | Q(id_estado_actividad=10))).count()
                ValEliminadas.append(val)


            context["valores"] = {"ValFinalizadas": ValFinalizadas,
                       "ValEnCurso": ValEnCurso,
                       "ValNoIniciado": ValNoIniciado,
                       "ValConRetraso": ValConRetraso,
                       "ValSinMovimiento": ValSinMovimiento,
                       "ValEliminadas": ValEliminadas,}



            context["qs"] = ps
            context["qs2"] = ps2
            context["UnidadesAsociadas"] = UnidadesAsociadas
            context['PeriodoActual'] = {'estado': periodo_actual}
            context["GrupoDashboard"] = 'GrupoAdmin'



            return context

        if Grupo.id == 1: #Si pertenece a un usuario que formula

            id_jefatura = Ges_Jefatura.objects.get(id_user=id_usuario_actual)
            try:
                id_controlador = Ges_Controlador.objects.get(
                    Q(id_jefatura=id_jefatura) & Q(id_periodo=periodo_actual.id))
            except IndexError:
                id_controlador = 0
                pass


            if id_controlador != 0:
                context['estado_flujo'] = {'estado': id_controlador.estado_flujo}
                context['estado_plan'] = {'estado': id_controlador.id_estado_plan}
            else:
                context['estado_flujo'] = {'estado': '-'}
                context['estado_plan'] = {'estado': '-'}


            try:
                estado_seguimiento = Glo_Seguimiento.objects.order_by('-id')[0]
            except IndexError:
                estado_seguimiento = 0
                pass

            if estado_seguimiento != 0:
                context['estado_seguimiento'] = {'estado': estado_seguimiento.id_estado_seguimiento}
            else:
                context['estado_seguimiento'] = {'estado': '-'}



            total_actividades = list(Ges_Actividad.objects.filter(Q(id_controlador=id_controlador) & Q(id_periodo=periodo_actual.id)).aggregate(Count('id')).values())[0]

            if total_actividades ==0: #Para que no divida por 0 en el caso que no posea actividades ingresadas.
                context['total_actividades'] = {'total': 0}
                total_actividades=1
            else:
                context['total_actividades'] = {'total': total_actividades}

            total_actividades_finalizadas = list(Ges_Actividad.objects.filter(
                Q(id_controlador=id_controlador) & Q(id_periodo=periodo_actual.id) & Q(id_estado_actividad=7)).aggregate(Count('id')).values())[0]
            total_actividades_en_curso = list(Ges_Actividad.objects.filter(
                Q(id_controlador=id_controlador) & Q(id_periodo=periodo_actual.id) & (Q(id_estado_actividad=3) | Q(id_estado_actividad=8))).aggregate(Count('id')).values())[0]
            total_actividades_no_iniciadas = list(Ges_Actividad.objects.filter(
                Q(id_controlador=id_controlador) & Q(id_periodo=periodo_actual.id) & Q(id_estado_actividad=4)).aggregate(Count('id')).values())[0]
            total_actividades_con_retraso = list(Ges_Actividad.objects.filter(
                Q(id_controlador=id_controlador) & Q(id_periodo=periodo_actual.id) & (Q(id_estado_actividad=1) | Q(id_estado_actividad=2))).aggregate(Count('id')).values())[0]
            total_actividades_sin_movimiento = list(Ges_Actividad.objects.filter(
                Q(id_controlador=id_controlador) & Q(id_periodo=periodo_actual.id) & (Q(id_estado_actividad=5) | Q(id_estado_actividad=6))).aggregate(Count('id')).values())[0]
            total_actividades_eliminadas = list(Ges_Actividad.objects.filter(
                Q(id_controlador=id_controlador) & Q(id_periodo=periodo_actual.id) & (Q(id_estado_actividad=9) | Q(id_estado_actividad=10))).aggregate(Count('id')).values())[0]



            context['actividades'] = {'total_finalizada': total_actividades_finalizadas,
                                      'total_finalizada_per': "{0:.2f}".format(((total_actividades_finalizadas*100)/total_actividades)),

                                      'total_en_curso': total_actividades_en_curso,
                                      'total_en_curso_per': "{0:.2f}".format(
                                          ((total_actividades_en_curso * 100) / total_actividades)),

                                      'total_no_iniciadas': total_actividades_no_iniciadas,
                                      'total_no_iniciadas_per': "{0:.2f}".format(
                                          ((total_actividades_no_iniciadas * 100) / total_actividades)),

                                      'total_con_retraso': total_actividades_con_retraso,
                                      'total_con_retraso_per': "{0:.2f}".format(
                                          ((total_actividades_con_retraso * 100) / total_actividades)),

                                      'total_sin_movimiento': total_actividades_sin_movimiento,
                                      'total_sin_movimiento_per': "{0:.2f}".format(
                                          ((total_actividades_sin_movimiento * 100) / total_actividades)),

                                      'total_eliminada': total_actividades_eliminadas,
                                      'total_eliminada_per': "{0:.2f}".format(
                                          ((total_actividades_eliminadas * 100) / total_actividades))

                                      }

            context["GrupoDashboard"] = 'GrupoFormula'
            return context


        if Grupo.id == 3: #Si pertenece a Jefatura Primer Nivel

            id_jefatura = Ges_Jefatura.objects.get(id_user=id_usuario_actual)

            NivelJef= id_jefatura.id_nivel.orden_nivel

            if NivelJef == 2:

                try:
                    estado_seguimiento = Glo_Seguimiento.objects.order_by('-id')[0]
                except IndexError:
                    estado_seguimiento = 0
                    pass

                if estado_seguimiento != 0:
                    context['estado_seguimiento'] = {'estado': estado_seguimiento.id_estado_seguimiento}
                else:
                    context['estado_seguimiento'] = {'estado': '-'}

                try:
                    estado_validacion = Glo_validacion.objects.order_by('-id')[0]
                except IndexError:
                    estado_validacion = 0
                    pass

                if estado_validacion != 0:
                    context['estado_validacion'] = {'estado': estado_validacion.id_estado_periodo}
                else:
                    context['estado_validacion'] = {'estado': '-'}

                idSegundoNivel = id_jefatura.id_nivel.id_segundo_nivel_id
                unidadesAsociadasTN = Ges_TercerNivel.objects.filter(
                    Q(id_periodo=periodo_actual) & Q(segundo_nivel_id=idSegundoNivel))
                # unidadesAsociadasCN = Ges_CuartoNivel.objects.filter(
                #     Q(id_periodo=periodo_actual) & Q(tercer_nivel_id__in=unidadesAsociadasTN))

                objetivosAsociados = Ges_Objetivo_TacticoTN.objects.filter(
                    Q(id_periodo=periodo_actual) & Q(id_tercer_nivel_id__in=unidadesAsociadasTN))

                total_actividades_por_el_departamento = list(
                    Ges_Actividad.objects.filter(
                        Q(id_periodo=periodo_actual) & Q(id_objetivo_tacticotn_id__in=objetivosAsociados)).aggregate(
                        Count('id')).values())[0]
                context['total_actividades_por_el_departamento'] = {'cantidad': total_actividades_por_el_departamento}

                GrafEstados = Ges_Actividad.objects.filter(
                    Q(id_periodo=periodo_actual) & Q(id_objetivo_tacticotn_id__in=objetivosAsociados)).values(
                    'id_estado_actividad__descripcion_estado').annotate(CantidadEst=Count('id')).order_by(
                    'id_estado_actividad__orden')  # estado por jefatura

                PlanesPorArea = Ges_Actividad.objects.filter(
                    Q(id_periodo=periodo_actual) & Q(id_objetivo_tacticotn_id__in=objetivosAsociados)).values(
                    'id_controlador__id_jefatura__id_nivel__descripcion_nivel',
                    'id_controlador__estado_flujo__descripcion_estado').annotate(
                    CantidadPlan=Count('id'))

                UnidadesAsociadas = Ges_Actividad.objects.filter(
                    Q(id_periodo=periodo_actual) & Q(id_objetivo_tacticotn_id__in=objetivosAsociados)).values(
                    'id_controlador__id_jefatura__id_nivel__descripcion_nivel').annotate(
                    CantidadPlan=Count('id')).order_by(
                    'id_controlador')

                controladores = list(Ges_Actividad.objects.filter(
                    Q(id_periodo=periodo_actual) & Q(id_objetivo_tacticotn_id__in=objetivosAsociados)).values_list(
                    'id_controlador', flat=True).distinct().order_by(
                    'id_controlador'))  ##Trae solo los controladores que han ingresado una actividad

                # controladores = list(Ges_Controlador.objects.filter(Q(id_periodo=periodo_actual)).values_list('id', flat=True).order_by(
                #     'id')) ##Trae todos los controladores sin importar sin ingresaron algo

                ValFinalizadas = []
                ValEnCurso = []
                ValNoIniciado = []
                ValConRetraso = []
                ValSinMovimiento = []
                ValEliminadas = []

                for i in controladores:
                    val = Ges_Actividad.objects.filter(
                        Q(id_controlador=i) & Q(id_periodo=periodo_actual) & Q(id_estado_actividad=7) & Q(
                            id_objetivo_tacticotn_id__in=objetivosAsociados)).count()
                    ValFinalizadas.append(val)

                    val = Ges_Actividad.objects.filter(
                        (Q(id_controlador=i) & Q(id_periodo=periodo_actual) & Q(
                            id_objetivo_tacticotn_id__in=objetivosAsociados)) & (
                                Q(id_estado_actividad=3) | Q(id_estado_actividad=8))).count()
                    ValEnCurso.append(val)

                    val = Ges_Actividad.objects.filter(
                        Q(id_controlador=i) & Q(id_periodo=periodo_actual) & Q(id_estado_actividad=4) & Q(
                            id_objetivo_tacticotn_id__in=objetivosAsociados)).count()
                    ValNoIniciado.append(val)

                    val = Ges_Actividad.objects.filter(
                        Q(id_controlador=i) & Q(id_periodo=periodo_actual) & (
                                Q(id_estado_actividad=1) | Q(id_estado_actividad=2)) & Q(
                            id_objetivo_tacticotn_id__in=objetivosAsociados)).count()
                    ValConRetraso.append(val)

                    val = Ges_Actividad.objects.filter(
                        Q(id_controlador=i) & Q(id_periodo=periodo_actual) & (
                                Q(id_estado_actividad=5) | Q(id_estado_actividad=6)) & Q(
                            id_objetivo_tacticotn_id__in=objetivosAsociados)).count()
                    ValSinMovimiento.append(val)

                    val = Ges_Actividad.objects.filter(
                        Q(id_controlador=i) & Q(id_periodo=periodo_actual) & (
                                Q(id_estado_actividad=9) | Q(id_estado_actividad=10)) & Q(
                            id_objetivo_tacticotn_id__in=objetivosAsociados)).count()
                    ValEliminadas.append(val)

                context["valores"] = {"ValFinalizadas": ValFinalizadas,
                                      "ValEnCurso": ValEnCurso,
                                      "ValNoIniciado": ValNoIniciado,
                                      "ValConRetraso": ValConRetraso,
                                      "ValSinMovimiento": ValSinMovimiento,
                                      "ValEliminadas": ValEliminadas, }

                context["GrafEstados"] = GrafEstados
                context["PlanesPorArea"] = PlanesPorArea
                context["UnidadesAsociadas"] = UnidadesAsociadas

                context["GrupoDashboard"] = 'GrupoJefeSegunda'


            if NivelJef == 3:

                try:
                    estado_seguimiento = Glo_Seguimiento.objects.order_by('-id')[0]
                except IndexError:
                    estado_seguimiento = 0
                    pass

                if estado_seguimiento != 0:
                    context['estado_seguimiento'] = {'estado': estado_seguimiento.id_estado_seguimiento}
                else:
                    context['estado_seguimiento'] = {'estado': '-'}

                try:
                    estado_validacion = Glo_validacion.objects.order_by('-id')[0]
                except IndexError:
                    estado_validacion = 0
                    pass

                if estado_validacion != 0:
                    context['estado_validacion'] = {'estado': estado_validacion.id_estado_periodo}
                else:
                    context['estado_validacion'] = {'estado': '-'}

                idTercerNivel = id_jefatura.id_nivel.id_tercer_nivel_id
                unidadesAsociadasCN= Ges_CuartoNivel.objects.filter(Q(id_periodo=periodo_actual) & Q(tercer_nivel_id=idTercerNivel))
                objetivosAsociados= Ges_Objetivo_Operativo.objects.filter(Q(id_periodo=periodo_actual) & Q(id_cuarto_nivel_id__in=unidadesAsociadasCN))
                # val5= Ges_Actividad.objects.filter(id_objetivo_operativo_id__in=val4)


                total_actividades_por_el_departamento = list(Ges_Actividad.objects.filter(Q(id_periodo=periodo_actual) & Q(id_objetivo_operativo_id__in=objetivosAsociados)).aggregate(Count('id')).values())[0]
                context['total_actividades_por_el_departamento'] = {'cantidad': total_actividades_por_el_departamento}


                GrafEstados = Ges_Actividad.objects.filter(Q(id_periodo=periodo_actual) & Q(id_objetivo_operativo_id__in=objetivosAsociados)).values(
                    'id_estado_actividad__descripcion_estado').annotate(CantidadEst=Count('id')).order_by(
                    'id_estado_actividad__orden')  # estado por jefatura

                PlanesPorArea = Ges_Actividad.objects.filter(
                    Q(id_periodo=periodo_actual) & Q(id_objetivo_operativo_id__in=objetivosAsociados)).values(
                    'id_controlador__id_jefatura__id_nivel__descripcion_nivel',
                    'id_controlador__estado_flujo__descripcion_estado').annotate(
                    CantidadPlan=Count('id'))

                UnidadesAsociadas = Ges_Actividad.objects.filter(Q(id_periodo=periodo_actual) & Q(id_objetivo_operativo_id__in=objetivosAsociados) ).values(
                    'id_controlador__id_jefatura__id_nivel__descripcion_nivel').annotate(
                    CantidadPlan=Count('id')).order_by(
                    'id_controlador')

                controladores = list(Ges_Actividad.objects.filter(Q(id_periodo=periodo_actual) & Q(id_objetivo_operativo_id__in=objetivosAsociados) ).values_list(
                    'id_controlador', flat=True).distinct().order_by(
                    'id_controlador'))##Trae solo los controladores que han ingresado una actividad

                # controladores = list(Ges_Controlador.objects.filter(Q(id_periodo=periodo_actual)).values_list('id', flat=True).order_by(
                #     'id')) ##Trae todos los controladores sin importar sin ingresaron algo

                ValFinalizadas = []
                ValEnCurso = []
                ValNoIniciado = []
                ValConRetraso = []
                ValSinMovimiento = []
                ValEliminadas = []

                for i in controladores:
                    val = Ges_Actividad.objects.filter(
                        Q(id_controlador=i) & Q(id_periodo=periodo_actual) & Q(id_estado_actividad=7)& Q(id_objetivo_operativo_id__in=objetivosAsociados)).count()
                    ValFinalizadas.append(val)

                    val = Ges_Actividad.objects.filter(
                        (Q(id_controlador=i) & Q(id_periodo=periodo_actual) &  Q(id_objetivo_operativo_id__in=objetivosAsociados)) & (Q(id_estado_actividad=3) | Q(id_estado_actividad=8))).count()
                    ValEnCurso.append(val)

                    val = Ges_Actividad.objects.filter(
                        Q(id_controlador=i) & Q(id_periodo=periodo_actual) & Q(id_estado_actividad=4) & Q(id_objetivo_operativo_id__in=objetivosAsociados)).count()
                    ValNoIniciado.append(val)

                    val = Ges_Actividad.objects.filter(
                        Q(id_controlador=i) & Q(id_periodo=periodo_actual) & (
                                    Q(id_estado_actividad=1) | Q(id_estado_actividad=2)) & Q(id_objetivo_operativo_id__in=objetivosAsociados)).count()
                    ValConRetraso.append(val)

                    val = Ges_Actividad.objects.filter(
                        Q(id_controlador=i) & Q(id_periodo=periodo_actual) & (
                                    Q(id_estado_actividad=5) | Q(id_estado_actividad=6)) & Q(id_objetivo_operativo_id__in=objetivosAsociados)).count()
                    ValSinMovimiento.append(val)

                    val = Ges_Actividad.objects.filter(
                        Q(id_controlador=i) & Q(id_periodo=periodo_actual) & (
                                    Q(id_estado_actividad=9) | Q(id_estado_actividad=10)) & Q(id_objetivo_operativo_id__in=objetivosAsociados)).count()
                    ValEliminadas.append(val)

                context["valores"] = {"ValFinalizadas": ValFinalizadas,
                                      "ValEnCurso": ValEnCurso,
                                      "ValNoIniciado": ValNoIniciado,
                                      "ValConRetraso": ValConRetraso,
                                      "ValSinMovimiento": ValSinMovimiento,
                                      "ValEliminadas": ValEliminadas, }


                context["GrafEstados"] = GrafEstados
                context["PlanesPorArea"] = PlanesPorArea
                context["UnidadesAsociadas"] = UnidadesAsociadas



            if NivelJef == 1: # Director(a)


                try:
                    estado_seguimiento = Glo_Seguimiento.objects.order_by('-id')[0]
                except IndexError:
                    estado_seguimiento = 0
                    pass

                if estado_seguimiento != 0:
                    context['estado_seguimiento'] = {'estado': estado_seguimiento.id_estado_seguimiento}
                else:
                    context['estado_seguimiento'] = {'estado': '-'}

                try:
                    estado_validacion = Glo_validacion.objects.order_by('-id')[0]
                except IndexError:
                    estado_validacion = 0
                    pass

                if estado_validacion != 0:
                    context['estado_validacion'] = {'estado': estado_validacion.id_estado_periodo}
                else:
                    context['estado_validacion'] = {'estado': '-'}

                idPrimerNivel = id_jefatura.id_nivel.id_primer_nivel_id
                unidadesAsociadasTN= Ges_SegundoNivel.objects.filter(Q(id_periodo=periodo_actual) & Q(primer_nivel_id=idPrimerNivel))
                objetivosAsociados= Ges_Objetivo_Tactico.objects.filter(Q(id_periodo=periodo_actual) & Q(id_segundo_nivel_id__in=unidadesAsociadasTN))
                # val5= Ges_Actividad.objects.filter(id_objetivo_operativo_id__in=val4)

                total_actividades_por_el_departamento = list(Ges_Actividad.objects.filter(Q(id_periodo=periodo_actual) & Q(id_objetivo_tactico_id__in=objetivosAsociados)).aggregate(Count('id')).values())[0]
                context['total_actividades_por_el_departamento'] = {'cantidad': total_actividades_por_el_departamento}


                GrafEstados = Ges_Actividad.objects.filter(Q(id_periodo=periodo_actual) & Q(id_objetivo_tactico_id__in=objetivosAsociados)).values(
                    'id_estado_actividad__descripcion_estado').annotate(CantidadEst=Count('id')).order_by(
                    'id_estado_actividad__orden')  # estado por jefatura

                PlanesPorArea = Ges_Actividad.objects.filter(
                    Q(id_periodo=periodo_actual) & Q(id_objetivo_tactico_id__in=objetivosAsociados)).values(
                    'id_controlador__id_jefatura__id_nivel__descripcion_nivel',
                    'id_controlador__estado_flujo__descripcion_estado').annotate(
                    CantidadPlan=Count('id'))

                UnidadesAsociadas = Ges_Actividad.objects.filter(Q(id_periodo=periodo_actual) & Q(id_objetivo_tactico_id__in=objetivosAsociados) ).values(
                    'id_controlador__id_jefatura__id_nivel__descripcion_nivel').annotate(
                    CantidadPlan=Count('id')).order_by(
                    'id_controlador')

                controladores = list(Ges_Actividad.objects.filter(Q(id_periodo=periodo_actual) & Q(id_objetivo_tactico_id__in=objetivosAsociados) ).values_list(
                    'id_controlador', flat=True).distinct().order_by(
                    'id_controlador'))##Trae solo los controladores que han ingresado una actividad

                # controladores = list(Ges_Controlador.objects.filter(Q(id_periodo=periodo_actual)).values_list('id', flat=True).order_by(
                #     'id')) ##Trae todos los controladores sin importar sin ingresaron algo

                ValFinalizadas = []
                ValEnCurso = []
                ValNoIniciado = []
                ValConRetraso = []
                ValSinMovimiento = []
                ValEliminadas = []

                for i in controladores:
                    val = Ges_Actividad.objects.filter(
                        Q(id_controlador=i) & Q(id_periodo=periodo_actual) & Q(id_estado_actividad=7)& Q(id_objetivo_tactico_id__in=objetivosAsociados)).count()
                    ValFinalizadas.append(val)

                    val = Ges_Actividad.objects.filter(
                        (Q(id_controlador=i) & Q(id_periodo=periodo_actual) &  Q(id_objetivo_tactico_id__in=objetivosAsociados)) & (Q(id_estado_actividad=3) | Q(id_estado_actividad=8))).count()
                    ValEnCurso.append(val)

                    val = Ges_Actividad.objects.filter(
                        Q(id_controlador=i) & Q(id_periodo=periodo_actual) & Q(id_estado_actividad=4) & Q(id_objetivo_tactico_id__in=objetivosAsociados)).count()
                    ValNoIniciado.append(val)

                    val = Ges_Actividad.objects.filter(
                        Q(id_controlador=i) & Q(id_periodo=periodo_actual) & (
                                    Q(id_estado_actividad=1) | Q(id_estado_actividad=2)) & Q(id_objetivo_tactico_id__in=objetivosAsociados)).count()
                    ValConRetraso.append(val)

                    val = Ges_Actividad.objects.filter(
                        Q(id_controlador=i) & Q(id_periodo=periodo_actual) & (
                                    Q(id_estado_actividad=5) | Q(id_estado_actividad=6)) & Q(id_objetivo_tactico_id__in=objetivosAsociados)).count()
                    ValSinMovimiento.append(val)

                    val = Ges_Actividad.objects.filter(
                        Q(id_controlador=i) & Q(id_periodo=periodo_actual) & (
                                    Q(id_estado_actividad=9) | Q(id_estado_actividad=10)) & Q(id_objetivo_tactico_id__in=objetivosAsociados)).count()
                    ValEliminadas.append(val)

                context["valores"] = {"ValFinalizadas": ValFinalizadas,
                                      "ValEnCurso": ValEnCurso,
                                      "ValNoIniciado": ValNoIniciado,
                                      "ValConRetraso": ValConRetraso,
                                      "ValSinMovimiento": ValSinMovimiento,
                                      "ValEliminadas": ValEliminadas, }


                context["GrafEstados"] = GrafEstados
                context["PlanesPorArea"] = PlanesPorArea
                context["UnidadesAsociadas"] = UnidadesAsociadas





            context["GrupoDashboard"] = 'GrupoJefeDirecto'

            return context

        if Grupo.id == 4:  # Si pertenece a Jefatura Segundo Nivel

            id_jefatura = Ges_Jefatura.objects.get(id_user=id_usuario_actual)

            try:
                estado_seguimiento = Glo_Seguimiento.objects.order_by('-id')[0]
            except IndexError:
                estado_seguimiento = 0
                pass

            if estado_seguimiento != 0:
                context['estado_seguimiento'] = {'estado': estado_seguimiento.id_estado_seguimiento}
            else:
                context['estado_seguimiento'] = {'estado': '-'}

            try:
                estado_validacion = Glo_validacion.objects.order_by('-id')[0]
            except IndexError:
                estado_validacion = 0
                pass

            if estado_validacion != 0:
                context['estado_validacion'] = {'estado': estado_validacion.id_estado_periodo}
            else:
                context['estado_validacion'] = {'estado': '-'}

            idSegundoNivel = id_jefatura.id_nivel.id_segundo_nivel_id
            unidadesAsociadasTN = Ges_TercerNivel.objects.filter(Q(id_periodo=periodo_actual) & Q(segundo_nivel_id=idSegundoNivel))
            unidadesAsociadasCN = Ges_CuartoNivel.objects.filter(Q(id_periodo=periodo_actual) & Q(tercer_nivel_id__in=unidadesAsociadasTN))

            objetivosAsociados = Ges_Objetivo_Operativo.objects.filter(Q(id_periodo=periodo_actual) & Q(id_cuarto_nivel_id__in=unidadesAsociadasCN))

            total_actividades_por_el_departamento = list(
                Ges_Actividad.objects.filter(Q(id_periodo=periodo_actual) & Q(id_objetivo_operativo_id__in=objetivosAsociados)).aggregate(
                    Count('id')).values())[0]
            context['total_actividades_por_el_departamento'] = {'cantidad': total_actividades_por_el_departamento}

            GrafEstadosSJ = Ges_Actividad.objects.filter(
                Q(id_periodo=periodo_actual) & Q(id_objetivo_operativo_id__in=objetivosAsociados)).values(
                'id_estado_actividad__descripcion_estado').annotate(CantidadEst=Count('id')).order_by(
                'id_estado_actividad__orden')  # estado por jefatura

            PlanesPorArea = Ges_Actividad.objects.filter(
                Q(id_periodo=periodo_actual) & Q(id_objetivo_operativo_id__in=objetivosAsociados)).values(
                'id_controlador__id_jefatura__id_nivel__descripcion_nivel',
                'id_controlador__estado_flujo__descripcion_estado').annotate(
                CantidadPlan=Count('id'))

            UnidadesAsociadas = Ges_Actividad.objects.filter(
                Q(id_periodo=periodo_actual) & Q(id_objetivo_operativo_id__in=objetivosAsociados)).values(
                'id_controlador__id_jefatura__id_nivel__descripcion_nivel').annotate(
                CantidadPlan=Count('id')).order_by(
                    'id_controlador')

            controladores = list(Ges_Actividad.objects.filter(
                Q(id_periodo=periodo_actual) & Q(id_objetivo_operativo_id__in=objetivosAsociados)).values_list(
                'id_controlador', flat=True).distinct().order_by(
                'id_controlador'))  ##Trae solo los controladores que han ingresado una actividad

            # controladores = list(Ges_Controlador.objects.filter(Q(id_periodo=periodo_actual)).values_list('id', flat=True).order_by(
            #     'id')) ##Trae todos los controladores sin importar sin ingresaron algo

            ValFinalizadas = []
            ValEnCurso = []
            ValNoIniciado = []
            ValConRetraso = []
            ValSinMovimiento = []
            ValEliminadas = []

            for i in controladores:
                val = Ges_Actividad.objects.filter(
                    Q(id_controlador=i) & Q(id_periodo=periodo_actual) & Q(id_estado_actividad=7) & Q(
                        id_objetivo_operativo_id__in=objetivosAsociados)).count()
                ValFinalizadas.append(val)

                val = Ges_Actividad.objects.filter(
                    (Q(id_controlador=i) & Q(id_periodo=periodo_actual) & Q(
                        id_objetivo_operativo_id__in=objetivosAsociados)) & (
                                Q(id_estado_actividad=3) | Q(id_estado_actividad=8))).count()
                ValEnCurso.append(val)

                val = Ges_Actividad.objects.filter(
                    Q(id_controlador=i) & Q(id_periodo=periodo_actual) & Q(id_estado_actividad=4) & Q(
                        id_objetivo_operativo_id__in=objetivosAsociados)).count()
                ValNoIniciado.append(val)

                val = Ges_Actividad.objects.filter(
                    Q(id_controlador=i) & Q(id_periodo=periodo_actual) & (
                            Q(id_estado_actividad=1) | Q(id_estado_actividad=2)) & Q(
                        id_objetivo_operativo_id__in=objetivosAsociados)).count()
                ValConRetraso.append(val)

                val = Ges_Actividad.objects.filter(
                    Q(id_controlador=i) & Q(id_periodo=periodo_actual) & (
                            Q(id_estado_actividad=5) | Q(id_estado_actividad=6)) & Q(
                        id_objetivo_operativo_id__in=objetivosAsociados)).count()
                ValSinMovimiento.append(val)

                val = Ges_Actividad.objects.filter(
                    Q(id_controlador=i) & Q(id_periodo=periodo_actual) & (
                            Q(id_estado_actividad=9) | Q(id_estado_actividad=10)) & Q(
                        id_objetivo_operativo_id__in=objetivosAsociados)).count()
                ValEliminadas.append(val)

            context["valores"] = {"ValFinalizadas": ValFinalizadas,
                                  "ValEnCurso": ValEnCurso,
                                  "ValNoIniciado": ValNoIniciado,
                                  "ValConRetraso": ValConRetraso,
                                  "ValSinMovimiento": ValSinMovimiento,
                                  "ValEliminadas": ValEliminadas, }

            context["GrafEstadosSJ"] = GrafEstadosSJ
            context["PlanesPorArea"] = PlanesPorArea
            context["UnidadesAsociadas"] = UnidadesAsociadas

            context["GrupoDashboard"] = 'GrupoJefeSegunda'

            return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(*args, **kwargs)
        template_name = self.template_name

        Grupo = Group.objects.get(user=self.request.user)

        if Grupo.id==2 or Grupo.id==5 or Grupo.id==6:  # Si pertenece a un usuario admin, plani y super
            template_name = 'dashboard/dashboard_admin.html'

        if Grupo.id == 1:  # Si pertenece a un usuario que formula
            template_name = 'dashboard/dashboard_formulador.html'

        if Grupo.id == 3:  # Si pertenece a jefatura primer nivel
            template_name = 'dashboard/dashboard_jefeprimer.html'

        if Grupo.id == 4:  # Si pertenece a jefatura segundo nivel
            template_name = 'dashboard/dashboard_jefesegundo.html'


        return render(request, template_name, context)

def export_users_xls(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="users.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Users')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Usuario', 'Nombres', 'Apellidos', 'Email', ]

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    rows = User.objects.all().values_list('username', 'first_name', 'last_name', 'email')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response

def modificar_estado(request, id):


    template_name = "dashboard/modal_mod.html"

    qs = Ges_Actividad.objects.get(id=id) #Cualquier QS con la que quiera obtener datos para enviar al modal.
    context = {"qs": qs} # aquí le envío lo que quiero al modal para que lo muestre, incluso una lista.

    if request.method == "POST": # aquí recojo lo que trae el modal

        codigo= request.POST['pid'] # aquí capturo lo que traigo del modal
        select = request.POST['seleccion']  # aquí capturo lo que traigo del modal

        Ges_Actividad.objects.filter(id=id).update( # aquí actualizo o agrego o elimino.
            horas_actividad=codigo, descripcion_actividad=select,
        )
        request.session['message_class'] = "alert alert-success" #Tipo mensaje
        messages.success(request, "Los datos fueron actualizados correctamente!") # mensaje
        return HttpResponseRedirect('/dashboard/PlanDashboard ') # Redirije a la pantalla principal

    return render(request, template_name, context)



