from django.shortcuts import render
from django.contrib.auth.models import User, Group
from apps.controlador.models import Ges_Controlador
from apps.actividades.models import Ges_Actividad
from apps.periodos.models import Glo_Seguimiento

from apps.jefaturas.models import Ges_Jefatura
from django.db.models import Subquery, OuterRef, Count, Max, Sum
from django.db.models import QuerySet
from django.db.models import Q
from apps.objetivos.models import Ges_Objetivo_Estrategico, Ges_Objetivo_Operativo, Ges_Objetivo_Tactico, Ges_Objetivo_TacticoTN
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

import datetime
from django.contrib.messages.views import SuccessMessageMixin

# Create your views here.


# Dirije al dashboard al momento del login además agrega la variable se sesión grupo #


class InicioDashboard(TemplateView):
    template_name = 'dashboard/dashboard.html'


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

            # ps = Ges_Actividad.objects.filter(id_periodo=3).values('id_controlador__id_jefatura__id_user__first_name','id_controlador__id_jefatura__id_user__last_name').annotate(CantidadAct=Count('id')) # Cantidad act. por jefatura

            ps = Ges_Actividad.objects.filter(id_periodo=periodo_actual).values('id_estado_actividad__descripcion_estado').annotate(CantidadEst=Count('id')).order_by('id_estado_actividad__orden') # estado por jefatura
            ps2 = Ges_Controlador.objects.filter(id_periodo=periodo_actual).values('estado_flujo__descripcion_estado').annotate(CantidadAct=Count('id'))# Cantidad act. por areas
            ps3 = Ges_Actividad.objects.filter(id_periodo=periodo_actual).values(
                'id_controlador__id_jefatura__id_nivel__descripcion_nivel').annotate(
                CantidadPlan=Count('id'))
            ps4 = Ges_Actividad.objects.filter(Q(id_periodo=periodo_actual) & (Q(id_estado_actividad=9) | Q(id_estado_actividad=7)) ).values(
                'id_controlador__id_jefatura__id_nivel__descripcion_nivel').annotate(
                CantidadPlanFin=Count('id'))


            context["qs"] = ps
            context["qs2"] = ps2
            context["qs3"] = ps3
            context["qs4"] = ps4
            context["GrupoDashboard"] = 'GrupoAdmin'

            return context

        if Grupo.id == 1: #Si pertenece a un usuario que formula
            id_jefatura = Ges_Jefatura.objects.get(id_user=id_usuario_actual)
            try:
                id_controlador = Ges_Controlador.objects.get(
                    Q(id_jefatura=id_jefatura) & Q(id_periodo=periodo_actual.id))
            except Ges_Controlador.DoesNotExist:
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
            except Glo_Seguimiento.DoesNotExist:
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



