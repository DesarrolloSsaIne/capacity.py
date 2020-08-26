from django.contrib import admin
from django.urls import path, include


urlpatterns = [

    path(r'periodos/', include('apps.periodos.urls')),


    path(r'accounts/', include('apps.registration.urls')),
    path(r'admin/', admin.site.urls),
    path(r'dashboard/', include('apps.dashboard.urls')),
    path(r'estructura/', include('apps.estructura.urls')),
    path(r'objetivos/', include('apps.objetivos.urls')),
    path(r'horas/', include('apps.gestion_horas.urls')),
    path(r'jefaturas/', include('apps.jefaturas.urls')),
    path(r'feriados/', include('apps.feriados.urls')),
    path(r'ejes/', include('apps.eje.urls')),
    path(r'vista_objetivos/', include('apps.vista_objetivos.urls')),
    path(r'familiadecargos/', include('apps.familia_cargo.urls')),

    path(r'periodicidad/', include('apps.periodicidad.urls')),
    path(r'productos/', include('apps.productos.urls')),
    path(r'estado_flujo/', include('apps.estado_flujo.urls')),
    path(r'controlador/', include('apps.controlador.urls')),
    path(r'actividades/', include('apps.actividades.urls')),
    path(r'valida_plan/', include('apps.valida_plan.urls')),
    path(r'valida_plan2/', include('apps.valida_plan2.urls')),
    path(r'perfiles/', include('apps.perfiles.urls')),

    path(r'revision_planificacion/', include('apps.revision_planificacion.urls')),
    path(r'seguimiento_formula/', include('apps.seguimiento_formula.urls')),
    path(r'reportes/', include('apps.reportes.urls')),
    path(r'valida_seguimiento/', include('apps.valida_seguimiento.urls')),
    path(r'planificacion_admin/', include('apps.planificacion_admin.urls')),





]




