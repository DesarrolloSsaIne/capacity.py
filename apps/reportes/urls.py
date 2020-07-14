from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import GeneraReportCurvaEjecucion, export_users_xls
from django.conf.urls import url, include
urlpatterns = [


 url(r'ReporteCurvaEjecucion', login_required(GeneraReportCurvaEjecucion.as_view()), name='ReportCurvaEjecucion'),
 #url(r'DatosGrafico', login_required(DatosGraficoList.as_view()), name='DatosReport'),
 url(r'ExportarXls', export_users_xls, name='export_xls'),

]