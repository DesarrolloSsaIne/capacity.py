from django.shortcuts import render

from apps.actividades.models import Ges_Actividad
from django.db.models import Q
from django.views.generic import TemplateView
from django.http import HttpResponse
import datetime
from apps.periodos.models import Glo_Periodos
from openpyxl import Workbook


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


        lista_datos = Ges_Actividad.objects.filter(id_periodo=periodo_actual)
        context['object_list'] = lista_datos

        return context





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







