from django.shortcuts import render
from django.contrib.auth.models import User, Group
from apps.controlador.models import Ges_Controlador
from apps.actividades.models import Ges_Actividad

from apps.jefaturas.models import Ges_Jefatura
from django.db.models import Subquery, OuterRef, Count
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


class ClubChartView(TemplateView):
    template_name = 'dashboard/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super(ClubChartView, self).get_context_data(**kwargs)
        # ps = Ges_Actividad.objects.filter(id_periodo=3).values('id_controlador__id_jefatura__id_user__first_name','id_controlador__id_jefatura__id_user__last_name').annotate(CantidadAct=Count('id')) # Cantidad act. por jefatura

        ps = Ges_Controlador.objects.filter(id_periodo=3).values('estado_flujo__descripcion_estado').annotate(CantidadEst=Count('id')) # estado por jefatura
        ps2 = Ges_Actividad.objects.filter(id_periodo=3).values('id_controlador__id_jefatura__id_nivel__descripcion_nivel').annotate(CantidadAct=Count('id'))# Cantidad act. por areas
        ps3 = Ges_Controlador.objects.filter(id_periodo=3).values(
            'analista_asignado__first_name','analista_asignado__last_name').annotate(
            CantidadPlan=Count('id'))  # Cantidad planes por analista


        meses=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        mesesacum = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

        ValMeses = []
        ValMesesAcum = []

        ValMesesEjec = []
        ValMesesAcumEjec = []


        mydate = datetime.datetime.now()
        Mes=mydate.month



        for i in meses:
            val = Ges_Actividad.objects.filter(Q(fecha_inicio_actividad__month=i) & Q(id_periodo=3)).count()
            ValMeses.append(val)


        for i in mesesacum:

            if i==0:
                ValMesesAcum.append(ValMeses[i])
            else:
                ValMesesAcum.append(ValMeses[i] + ValMesesAcum[i-1])


        for i in meses:
            val = Ges_Actividad.objects.filter(Q(fecha_inicio_actividad__month=i) & Q(id_periodo=3) & (Q(id_estado_actividad_id=6) | Q(id_estado_actividad_id=7))).count()
            ValMesesEjec.append(val)

        for i in range(0, Mes):
            if i==0:
                ValMesesAcumEjec.append(ValMesesEjec[i])
            else:
                ValMesesAcumEjec.append(ValMesesEjec[i] + ValMesesAcumEjec[i-1])

        context["qs"] = ps
        context["qs2"] = ps2
        context["qs3"] = ps3
        context = {"ValMesesAcum":ValMesesAcum, "ValMesesAcumEjec":ValMesesAcumEjec,

                   }
        return context



# def export_users_csv(request):
#     response = HttpResponse(content_type='text/csv')
#     response['Content-Disposition'] = 'attachment; filename="users.csv"'
#
#     writer = csv.writer(response)
#     writer.writerow(['Username', 'First name', 'Last name', 'Email address'])
#
#     users = User.objects.all().values_list('username', 'first_name', 'last_name', 'email')
#     for user in users:
#         writer.writerow(user)
#
#     return response


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


    # class ClubChartView(TemplateView):
    #     template_name = 'dashboard/dashboard.html'
    #
    #     def get_context_data(self, **kwargs):
    #         context = super().get_context_data(**kwargs)
    #
    #         # context= Ges_Actividad.objects.annotate(num_act=Count('id_controlador'))
    #
    #         contexto = Ges_Actividad.objects.all()
    #         context["qs"] = contexto
    #         return context



    # def Char_Uno(request):
    #     labels = []
    #     data = []

    # queryset = Ges_Actividad.objects.filter(id_periodo=3)
    #
    # for city in queryset:
    #     labels.append(str(city.id_controlador.id_jefatura.id_nivel))
    #     data.append(city.total_horas)
    #
    # return render(request, 'dashboard/dashboard.html', {
    #     'labels': labels,
    #     'Midata': data,
    # })


def ir_dashboard(request):
    Grupo = Group.objects.filter(user=request.user)

    for MiGrupo in Grupo:
        result = str(MiGrupo)
        request.session['grupo']= result

    return render(request, 'dashboard/dashboard2.html')


