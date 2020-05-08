from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import ir_dashboard, ClubChartView,  export_users_xls,modificar_estado
from django.conf.urls import url, include
urlpatterns = [

 path(r'', login_required(ir_dashboard), name="dashboard"),

 #path('PlanDashboard', login_required(Char_Uno), name="plandashboard"),
 #path('PlanDashboard', login_required(ClubChartView), name="plandashboard"),
 url(r'PlanDashboard', login_required(ClubChartView.as_view()), name='plandashboard'),
 url(r'ExportarCsv', export_users_xls, name='export_users_csv'),
 path('modificar/<int:id>', modificar_estado, name="modificar"),
]
