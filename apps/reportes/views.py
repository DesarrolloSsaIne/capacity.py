from django.shortcuts import render
from django.contrib.auth.models import User, Group
from apps.controlador.models import Ges_Controlador
from apps.actividades.models import Ges_Actividad

from django.views.generic import ListView
from django.db.models import Q

from django.views.generic import TemplateView
from django.contrib.auth.models import User

import xlwt
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.contrib import messages

from django.db.models import Count
import datetime, xlsxwriter
from apps.periodos.models import Glo_Periodos
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, Border, Side, PatternFill

# Create your views here.
class GeneraReportCurvaEjecucion(TemplateView):
    template_name = 'reportes/report_seguimiento.html'

    def get_context_data(self, **kwargs):
        context = super(GeneraReportCurvaEjecucion, self).get_context_data(**kwargs)

        try:
            periodo_actual = Glo_Periodos.objects.get(id_estado=1)
        except Glo_Periodos.DoesNotExist:
            return None

        meses=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        mesesacum = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

        ValMeses = []
        ValMesesAcum = []

        ValMesesEjec = []
        ValMesesAcumEjec = []


        mydate = datetime.datetime.now()
        Mes=mydate.month



        for i in meses:
            val = Ges_Actividad.objects.filter(Q(fecha_inicio_actividad__month=i) & Q(id_periodo=periodo_actual)).count()
            ValMeses.append(val)


        for i in mesesacum:

            if i==0:
                ValMesesAcum.append(ValMeses[i])
            else:
                ValMesesAcum.append(ValMeses[i] + ValMesesAcum[i-1])


        for i in meses:
            val = Ges_Actividad.objects.filter(Q(fecha_inicio_actividad__month=i) & Q(id_periodo=periodo_actual) & (Q(id_estado_actividad_id=6) | Q(id_estado_actividad_id=7))).count()
            ValMesesEjec.append(val)

        for i in range(0, Mes):
            if i==0:
                ValMesesAcumEjec.append(ValMesesEjec[i])
            else:
                ValMesesAcumEjec.append(ValMesesEjec[i] + ValMesesAcumEjec[i-1])

        context = {"ValMesesAcum":ValMesesAcum,
                   "ValMesesAcumEjec":ValMesesAcumEjec, }
        a='ReporteCurvaEjecucion'

        lista_datos = Ges_Actividad.objects.filter(id_periodo=periodo_actual)
        context['object_list'] = lista_datos

        return context



# class DatosGraficoList(ListView):
#     model = Ges_Actividad
#     template_name = 'reportes/report_seguimiento.html'
#
#     def get_context_data(self, **kwargs):
#         context = super(DatosGraficoList, self).get_context_data(**kwargs)
#
#         try:
#             periodo_actual = Glo_Periodos.objects.get(id_estado=1)
#         except Glo_Periodos.DoesNotExist:
#             return None
#
#         lista_datos = Ges_Actividad.objects.filter(id=41)
#         context['object_list'] = lista_datos
#         return context





# class ClubChartView(TemplateView):
#     template_name = 'dashboard/dashboard.html'
#
#     def get_context_data(self, **kwargs):
#         context = super(ClubChartView, self).get_context_data(**kwargs)
#         # ps = Ges_Actividad.objects.filter(id_periodo=3).values('id_controlador__id_jefatura__id_user__first_name','id_controlador__id_jefatura__id_user__last_name').annotate(CantidadAct=Count('id')) # Cantidad act. por jefatura
#
#         ps = Ges_Controlador.objects.filter(id_periodo=3).values('estado_flujo__descripcion_estado').annotate(CantidadEst=Count('id')) # estado por jefatura
#         ps2 = Ges_Actividad.objects.filter(id_periodo=3).values('id_controlador__id_jefatura__id_nivel__descripcion_nivel').annotate(CantidadAct=Count('id'))# Cantidad act. por areas
#         ps3 = Ges_Controlador.objects.filter(id_periodo=3).values(
#             'analista_asignado__first_name','analista_asignado__last_name').annotate(
#             CantidadPlan=Count('id'))  # Cantidad planes por analista
#
#
#         meses=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
#         mesesacum = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
#
#         ValMeses = []
#         ValMesesAcum = []
#
#         ValMesesEjec = []
#         ValMesesAcumEjec = []
#
#
#         mydate = datetime.datetime.now()
#         Mes=mydate.month
#
#
#
#         for i in meses:
#             val = Ges_Actividad.objects.filter(Q(fecha_inicio_actividad__month=i) & Q(id_periodo=3)).count()
#             ValMeses.append(val)
#
#
#         for i in mesesacum:
#
#             if i==0:
#                 ValMesesAcum.append(ValMeses[i])
#             else:
#                 ValMesesAcum.append(ValMeses[i] + ValMesesAcum[i-1])
#
#
#         for i in meses:
#             val = Ges_Actividad.objects.filter(Q(fecha_inicio_actividad__month=i) & Q(id_periodo=3) & (Q(id_estado_actividad_id=6) | Q(id_estado_actividad_id=7))).count()
#             ValMesesEjec.append(val)
#
#         for i in range(0, Mes):
#             if i==0:
#                 ValMesesAcumEjec.append(ValMesesEjec[i])
#             else:
#                 ValMesesAcumEjec.append(ValMesesEjec[i] + ValMesesAcumEjec[i-1])
#
#         context["qs"] = ps
#         context["qs2"] = ps2
#         context["qs3"] = ps3
#         context = {"ValMesesAcum":ValMesesAcum, "ValMesesAcumEjec":ValMesesAcumEjec,
#
#                    }
#         return context
#
#
#

# import io
#
# from django.http.response import HttpResponse
#
# from xlsxwriter.workbook import Workbook
#
#
# def export_users_xls(request):
#
#     output = io.BytesIO()
#
#     workbook = Workbook(output, {'in_memory': True})
#     worksheet = workbook.add_worksheet()
#
#     # Some data we want to write to the worksheet.
#     expenses = (
#         ['Rent', 1000],
#         ['Gas', 100],
#         ['Food', 300],
#         ['Gym', 50],
#     )
#
#     # Start from the first cell. Rows and columns are zero indexed.
#     row = 0
#     col = 0
#
#     # Iterate over the data and write it out row by row.
#     for item, cost in (expenses):
#         worksheet.write(row, col, item)
#         worksheet.write(row, col + 1, cost)
#         row += 1
#
#     # Write a total using a formula.
#     worksheet.write(row, 0, 'Total')
#     worksheet.write(row, 1, '=SUMA(B1:B4)')
#
#
#
#
#
#
#
#     workbook.close()
#
#     output.seek(0)
#
#     response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
#     response['Content-Disposition'] = "attachment; filename=test.xlsx"
#
#     output.close()
#
#     return response

#
# import io
#
# from django.http.response import HttpResponse
#
# from xlsxwriter.workbook import Workbook
# def export_users_xls(request):
#     # Create an in-memory output file for the new workbook.
#     output = io.BytesIO()
#
#     # Even though the final file will be in memory the module uses temp
#     # files during assembly for efficiency. To avoid this on servers that
#     # don't allow temp files, for example the Google APP Engine, set the
#     # 'in_memory' Workbook() constructor option as shown in the docs.
#     workbook = xlsxwriter.Workbook(output)
#     worksheet = workbook.add_worksheet()
#
#     formatdict = {'num_format': 'mm/dd/yyyy'}
#     fmt = workbook.add_format(formatdict)
#     worksheet.set_column('A:A', None, fmt)
#
#     # worksheet.write('A1', 'des')
#     # worksheet.write('B1', 'fec')
#
#
#     # Get some data to write to the spreadsheet.
#     data = Ges_Actividad.objects.all().values_list('fecha_inicio_actividad')
#
#
#     for row_num, columns in enumerate(data):
#         for col_num, cell_data in enumerate(columns):
#             worksheet.write(row_num, col_num, cell_data)
#
#
#
#
#     # Close the workbook before sending the data.
#     workbook.close()
#
#     # Rewind the buffer.
#     output.seek(0)
#
#     # Set up the Http response.
#     filename = 'django_simple.xlsx'
#     response = HttpResponse(
#         output,
#         content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
#     )
#     response['Content-Disposition'] = 'attachment; filename=%s' % filename
#
#     return response


def export_users_xls(request):
    """
    Downloads all movies as Excel file with a single worksheet
    """
    actividades = Ges_Actividad.objects.all()


    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    )
    response['Content-Disposition'] = 'attachment; filename={date}-reporte_seguimiento.xlsx'.format(
        date=datetime.datetime.now().strftime('%d/%m/%Y'),
    )
    workbook = Workbook()


    # Get active worksheet/tab
    worksheet = workbook.active
    worksheet.title = 'reporte_seguimiento'

    # Define the titles for columns

    columns = ['Actividad',
               'Objetivo Vinculado',
               'Periodicidad',
               'Producto Estadístico',
               'Hora x Actividad',
               'Volumen',
               'N° Personas Asignadas',
               'Total Horas',
               'Cargo',
               'Fecha Incio Actividad',
               'Fecha Término Actividad',
               'Estado Actividad',
               'Fecha Real Finalización',
               'Reprogramación Fecha Inicio',
               'Reprogramación Fecha Término',
               'Justificación Desviación',
               'Dependencia 1',
               'Dependencia 2',
               'Área',
               'Eje'
               ]

    row_num = 1

    # Assign the titles for each cell of the header
    for col_num, column_title in enumerate(columns, 1):
        cell = worksheet.cell(row=row_num, column=col_num)
        cell.value = column_title

    # Iterate through all movies
    for actividad in actividades:
        row_num += 1
        #
        # Define the data for each cell in the row

        Nivel=actividad.id_controlador.nivel_inicial

        if Nivel==4:

            row = [

                actividad.descripcion_actividad,
                str(actividad.id_objetivo_operativo) ,
                str(actividad.id_periodicidad),
                str(actividad.id_producto_estadistico),
                actividad.horas_actividad,
                actividad.volumen,
                actividad.personas_asignadas,
                actividad.total_horas,
                str(actividad.id_familia_cargo),
                actividad.fecha_inicio_actividad,
                actividad.fecha_termino_actividad,
                str(actividad.id_estado_actividad),
                actividad.fecha_real_termino,
                actividad.fecha_reprogramacion_inicio,
                actividad.fecha_reprogramacion_termino,
                actividad.justificacion,
                str(actividad.id_objetivo_operativo.id_cuarto_nivel.tercer_nivel.segundo_nivel),
                str(actividad.id_objetivo_operativo.id_cuarto_nivel.tercer_nivel),
                str(actividad.id_objetivo_operativo.id_cuarto_nivel),
                str(actividad.id_objetivo_operativo.id_objetivo_tacticotn.id_objetivo_tactico.id_objetivo_estrategico.ges_eje),


            ]

        if Nivel==3:

            row = [

                actividad.descripcion_actividad,
                str(actividad.id_objetivo_tacticotn) ,
                str(actividad.id_periodicidad),
                str(actividad.id_producto_estadistico),
                actividad.horas_actividad,
                actividad.volumen,
                actividad.personas_asignadas,
                actividad.total_horas,
                str(actividad.id_familia_cargo),
                actividad.fecha_inicio_actividad,
                actividad.fecha_termino_actividad,
                str(actividad.id_estado_actividad),
                actividad.fecha_real_termino,
                actividad.fecha_reprogramacion_inicio,
                actividad.fecha_reprogramacion_termino,
                actividad.justificacion,
                str(actividad.id_objetivo_tacticotn.id_tercer_nivel.segundo_nivel),
                str(actividad.id_objetivo_tacticotn.id_tercer_nivel),
                str('-'),
                str(actividad.id_objetivo_tacticotn.id_objetivo_tactico.id_objetivo_estrategico.ges_eje),


            ]



        if Nivel==2:

            row = [

                actividad.descripcion_actividad,
                str(actividad.id_objetivo_tactico) ,
                str(actividad.id_periodicidad),
                str(actividad.id_producto_estadistico),
                actividad.horas_actividad,
                actividad.volumen,
                actividad.personas_asignadas,
                actividad.total_horas,
                str(actividad.id_familia_cargo),
                actividad.fecha_inicio_actividad,
                actividad.fecha_termino_actividad,
                str(actividad.id_estado_actividad),
                actividad.fecha_real_termino,
                actividad.fecha_reprogramacion_inicio,
                actividad.fecha_reprogramacion_termino,
                actividad.justificacion,
                str(actividad.id_objetivo_tactico.id_segundo_nivel),
                str('-'),
                str('-'),
                str(actividad.id_objetivo_tactico.id_objetivo_estrategico.ges_eje),


            ]




        # Assign the data for each cell of the row
        for col_num, cell_value in enumerate(row, 1):
            cell = worksheet.cell(row=row_num, column=col_num)
            cell.value = cell_value


            if col_num == 10:
                cell.number_format = 'dd/mm/yyyy'
            if col_num == 11:
                cell.number_format = 'dd/mm/yyyy'
            if col_num == 13:
                cell.number_format = 'dd/mm/yyyy'
            if col_num == 14:
                cell.number_format = 'dd/mm/yyyy'
            if col_num == 15:
                cell.number_format = 'dd/mm/yyyy'





    workbook.save(response)

    return response













# def export_users_xls(request):
#
#
#     response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
#     response['Content-Disposition'] = 'attachment; filename="users.xls"'
#
#     wb = xlwt.Workbook(encoding='utf-8')
#     ws = wb.add_sheet('Users')
#
#
#     # Sheet header, first row
#     row_num = 0
#
#     font_style = xlwt.XFStyle()
#     font_style.font.bold = True
#     style1 = xlwt.easyxf(num_format_str='D-MMM-YY')
#
#     ws.write(1, 0, datetime.datetime.now(), style1)
#
#     columns = ['Actividad',
#                'Objetivo Vinculado',
#                'Periodicidad',
#                'Producto Estadístico',
#                'Hora x Actividad',
#                'Volumen',
#                'N° Personas Asignadas',
#                'Total Horas',
#                'Cargo',
#                'Fecha Incio Actividad',
#                'Fecha Término Actividad',
#                'Estado Actividad']
#
#
#     for col_num in range(len(columns)):
#
#         ws.write(row_num, col_num, columns[col_num], font_style)
#
#     # Sheet body, remaining rows
#     font_style = xlwt.XFStyle()
#
#
#
#
#     a=4
#     if a==4:
#         rows = Ges_Actividad.objects.filter(id=46).values_list('descripcion_actividad',
#                                                                'id_objetivo_operativo__descripcion_objetivo',
#                                                                'id_periodicidad__descripcion_periodicidad',
#                                                                'id_producto_estadistico__descripcion_producto',
#                                                                'horas_actividad',
#                                                                'volumen',
#                                                                'personas_asignadas',
#                                                                'total_horas',
#                                                                'id_familia_cargo__descripcion_familiacargo',
#
#                                                                'fecha_inicio_actividad',
#                                                                'fecha_termino_actividad',
#                                                                'id_estado_actividad__descripcion_estado')
#
#
#         for row in rows:
#             row_num += 1
#             for col_num in range(len(row)):
#                 ws.write(row_num, col_num, row[col_num], font_style)
#
#
#
#     wb.save(response)
#     return response


# import csv
#
# def export_users_xls(request):
#     response = HttpResponse(content_type='text/csv')
#     response['Content-Disposition'] = 'attachment; filename="users.csv"'
#
#     writer = csv.writer(response)
#     writer.writerow(['Actividad', 'Fecha'])
#
#     rows = Ges_Actividad.objects.filter(id=46).values_list('descripcion_actividad', 'fecha_inicio_actividad')
#     for user in rows:
#          writer.writerow(user)
#        # writer.writerow([user.descripcion_actividad, user.fecha_inicio_actividad, ])
#
#     return response




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






