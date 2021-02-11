from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from apps.gestion_horas.models import Ges_Registro_Horas
from apps.feriados.models import Ges_Feriados
from apps.jefaturas.models import Ges_Jefatura
from apps.estructura.models import Ges_Niveles
from apps.controlador.models import Ges_Controlador
from django.db.models import Sum
from django.db.models import Q
from apps.gestion_horas.forms import GestionHorasForm, GestionHorasUpdateForm
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models.deletion import ProtectedError
from django.template import loader, Context
from django.contrib.auth.models import User
import datetime
from datetime import date
from apps.periodos.models import Glo_Periodos



def workdays(d, end, excluded=(6, 7)):
    days = []
    while d.date() <= end.date():
        if d.isoweekday() not in excluded:
            days.append(d)
        d += datetime.timedelta(days=1)
    return days


class RegistroHorasList(ListView):
    model = Ges_Registro_Horas
    template_name = 'registro_horas/registro_horas_list.html'


    def get_context_data(self,  **kwargs):
        context = super(RegistroHorasList, self).get_context_data(**kwargs)
        id_usuario_actual= self.request.user.id #obtiene id usuario actual


        try:
            periodo_actual = Glo_Periodos.objects.get(id_estado=1)
        except Glo_Periodos.DoesNotExist:
            return None


        try:
            id_jefatura=Ges_Jefatura.objects.get(Q(id_user=id_usuario_actual)  & Q(id_periodo=periodo_actual.id))
        except Ges_Jefatura.DoesNotExist:
            context['habilitado'] = {'mensaje': False}
            return None

        try:
            usuario_controlador= Ges_Controlador.objects.get(id_jefatura=id_jefatura.id)
        except Ges_Controlador.DoesNotExist:
            usuario_controlador= 0
            pass


        Unidad= Ges_Jefatura.objects.filter(id_user_id=id_usuario_actual).values('id_nivel__descripcion_nivel')


        if usuario_controlador == 0:
            context['error'] = {'id': 1}
            return context
            #sys.exit(1)
        else:

            nivel_usuario= Ges_Jefatura.objects.get(id_user=usuario_controlador.id_jefatura.id_user)

            lista_horas = Ges_Registro_Horas.objects.filter(Q(id_nivel=nivel_usuario.id_nivel) & Q(id_periodo=periodo_actual.id))

            dias_totales = list(
                Ges_Registro_Horas.objects.filter(Q(id_nivel=nivel_usuario.id_nivel) & Q(id_periodo=periodo_actual.id)).aggregate(Sum('dias_habiles')).values())[
                0]
            analistas_totales = list(
                Ges_Registro_Horas.objects.filter(Q(id_familiacargo=1) & Q(id_nivel=nivel_usuario.id_nivel) & Q(id_periodo=periodo_actual.id)).aggregate(Sum('dias_habiles')).values())[
                0]
            coordinadores_totales = list(
                Ges_Registro_Horas.objects.filter(Q(id_familiacargo=2) & Q(id_nivel=nivel_usuario.id_nivel) & Q(id_periodo=periodo_actual.id)).aggregate(Sum('dias_habiles')).values())[
                0]
            if dias_totales is None:
                horas_totales = 0
            else:
                 horas_totales= dias_totales * 8

            context['nivel'] = Unidad

            context['estado'] = {'estado': usuario_controlador.estado_flujo}
            context['object_list'] = lista_horas
            context['calculo'] = {'dias_totales': dias_totales ,
                                  'horas_totales': horas_totales,
                                  'analistas_totales':analistas_totales,
                                  'coordinadores_totales':coordinadores_totales,
                                  'usuario_controlador': usuario_controlador}

            context['habilitado'] = {'mensaje': True}

            return context






class RegistroHorasDetalle(ListView):
    model = Ges_Registro_Horas
    template_name = 'registro_horas/registro_horas_detalle.html'

    def get_context_data(self,  **kwargs):
        context = super(RegistroHorasDetalle, self).get_context_data(**kwargs)
        id_usuario_actual= self.request.user.id #obtiene id usuario actual

        try:
            periodo_actual = Glo_Periodos.objects.get(id_estado=1)
        except Glo_Periodos.DoesNotExist:
            return None

        try:
            id_jefatura = Ges_Jefatura.objects.get(Q(id_user=id_usuario_actual)  & Q(id_periodo=periodo_actual.id))
        except Ges_Jefatura.DoesNotExist:
            context['habilitado'] = {'mensaje': False}
            return None

        try:
            usuario_controlador = Ges_Controlador.objects.get(Q(id_jefatura=id_jefatura.id)  & Q(id_periodo=periodo_actual.id))
        except Ges_Controlador.DoesNotExist:
            context['habilitado'] = {'mensaje': False}
            return None

        nivel_usuario = Ges_Jefatura.objects.get(id_user=usuario_controlador.id_jefatura.id_user)



        try:
            lista_horas = Ges_Registro_Horas.objects.filter(Q(id_nivel=nivel_usuario.id_nivel) & Q(id_periodo=periodo_actual.id))
        except Ges_Registro_Horas.DoesNotExist:
            lista_horas = None

        dias_totales = list(
            Ges_Registro_Horas.objects.filter(Q(id_nivel=nivel_usuario.id_nivel) & Q(id_periodo=periodo_actual.id)).aggregate(Sum('dias_habiles')).values())[
            0]
        jefe_departamento_totales = list(
            Ges_Registro_Horas.objects.filter(Q(id_familiacargo=1) & Q(id_nivel=nivel_usuario.id_nivel) & Q(id_periodo=periodo_actual.id)).aggregate(Sum('dias_habiles')).values())[
            0]
        jefe_subdepartamento_totales = list(
            Ges_Registro_Horas.objects.filter(Q(id_familiacargo=2) & Q(id_nivel=nivel_usuario.id_nivel) & Q(id_periodo=periodo_actual.id)).aggregate(Sum('dias_habiles')).values())[
            0]
        coordinadores_totales = list(
            Ges_Registro_Horas.objects.filter(Q(id_familiacargo=3) & Q(id_nivel=nivel_usuario.id_nivel) & Q(id_periodo=periodo_actual.id)).aggregate(Sum('dias_habiles')).values())[
            0]
        supervisores_totales = list(
            Ges_Registro_Horas.objects.filter(Q(id_familiacargo=4) & Q(id_nivel=nivel_usuario.id_nivel) & Q(id_periodo=periodo_actual.id)).aggregate(Sum('dias_habiles')).values())[
            0]
        analistas_especialistar_totales = list(
            Ges_Registro_Horas.objects.filter(Q(id_familiacargo=5) & Q(id_nivel=nivel_usuario.id_nivel) & Q(id_periodo=periodo_actual.id)).aggregate(
                Sum('dias_habiles')).values())[
            0]
        analistas_totales = list(
            Ges_Registro_Horas.objects.filter(Q(id_familiacargo=6) & Q(id_nivel=nivel_usuario.id_nivel) & Q(id_periodo=periodo_actual.id)).aggregate(
                Sum('dias_habiles')).values())[
            0]
        supervisores_operativos_totales = list(
            Ges_Registro_Horas.objects.filter(Q(id_familiacargo=7) & Q(id_nivel=nivel_usuario.id_nivel) & Q(id_periodo=periodo_actual.id)).aggregate(
                Sum('dias_habiles')).values())[
            0]
        operativos_totales = list(
            Ges_Registro_Horas.objects.filter(Q(id_familiacargo=8) & Q(id_nivel=nivel_usuario.id_nivel) & Q(id_periodo=periodo_actual.id)).aggregate(
                Sum('dias_habiles')).values())[
            0]
        asistentes_totales = list(
            Ges_Registro_Horas.objects.filter(Q(id_familiacargo=9) & Q(id_nivel=nivel_usuario.id_nivel) & Q(id_periodo=periodo_actual.id)).aggregate(
                Sum('dias_habiles')).values())[
            0]
        auxiliares_totales = list(
            Ges_Registro_Horas.objects.filter(Q(id_familiacargo=10) & Q(id_nivel=nivel_usuario.id_nivel) & Q(id_periodo=periodo_actual.id)).aggregate(
                Sum('dias_habiles')).values())[
            0]



        jefe_departamento_horas = list(
            Ges_Registro_Horas.objects.filter(Q(id_familiacargo=1) & Q(id_nivel=nivel_usuario.id_nivel) & Q(id_periodo=periodo_actual.id)).aggregate(Sum('dias_habiles')).values())[
            0]

        if jefe_departamento_horas is None:
            jefe_departamento_horas =0
        else:
            jefe_departamento_horas= jefe_departamento_horas * 8


        jefe_subdepartamento_horas = list(
            Ges_Registro_Horas.objects.filter(Q(id_familiacargo=2) & Q(id_nivel=nivel_usuario.id_nivel) & Q(id_periodo=periodo_actual.id)).aggregate(Sum('dias_habiles')).values())[
            0]

        if jefe_subdepartamento_horas is None:
            jefe_subdepartamento_horas =0
        else:
            jefe_subdepartamento_horas= jefe_subdepartamento_horas * 8


        coordinadores_horas = list(
            Ges_Registro_Horas.objects.filter(Q(id_familiacargo=3) & Q(id_nivel=nivel_usuario.id_nivel) & Q(id_periodo=periodo_actual.id)).aggregate(Sum('dias_habiles')).values())[
            0]

        if coordinadores_horas is None:
            coordinadores_horas =0
        else:
            coordinadores_horas= coordinadores_horas * 8


        supervisores_horas = list(
            Ges_Registro_Horas.objects.filter(Q(id_familiacargo=4) & Q(id_nivel=nivel_usuario.id_nivel) & Q(id_periodo=periodo_actual.id)).aggregate(Sum('dias_habiles')).values())[
            0]

        if supervisores_horas is None:
            supervisores_horas =0
        else:
            supervisores_horas= supervisores_horas * 8

        analistas_especialistar_horas = list(
            Ges_Registro_Horas.objects.filter(Q(id_familiacargo=5) & Q(id_nivel=nivel_usuario.id_nivel) & Q(id_periodo=periodo_actual.id)).aggregate(
                Sum('dias_habiles')).values())[
            0]

        if analistas_especialistar_horas is None:
            analistas_especialistar_horas = 0
        else:
            analistas_especialistar_horas= analistas_especialistar_horas * 8


        analistas_horas = list(
            Ges_Registro_Horas.objects.filter(Q(id_familiacargo=6) & Q(id_nivel=nivel_usuario.id_nivel) & Q(id_periodo=periodo_actual.id)).aggregate(
                Sum('dias_habiles')).values())[
            0]

        if analistas_horas is None:
            analistas_horas = 0
        else:
            analistas_horas= analistas_horas * 8


        supervisores_operativos_horas = list(
            Ges_Registro_Horas.objects.filter(Q(id_familiacargo=7) & Q(id_nivel=nivel_usuario.id_nivel) & Q(id_periodo=periodo_actual.id)).aggregate(
                Sum('dias_habiles')).values())[
            0]

        if supervisores_operativos_horas is None:
            supervisores_operativos_horas = 0
        else:
            supervisores_operativos_horas= supervisores_operativos_horas * 8


        operativos_horas = list(
            Ges_Registro_Horas.objects.filter(Q(id_familiacargo=8) & Q(id_nivel=nivel_usuario.id_nivel) & Q(id_periodo=periodo_actual.id)).aggregate(
                Sum('dias_habiles')).values())[
            0]

        if operativos_horas is None:
            operativos_horas = 0
        else:
            operativos_horas= operativos_horas * 8

        asistentes_horas = list(
            Ges_Registro_Horas.objects.filter(Q(id_familiacargo=9) & Q(id_nivel=nivel_usuario.id_nivel) & Q(id_periodo=periodo_actual.id)).aggregate(
                Sum('dias_habiles')).values())[
            0]

        if asistentes_horas is None:
            asistentes_horas = 0
        else:
            asistentes_horas= asistentes_horas * 8


        auxiliares_horas= list(
            Ges_Registro_Horas.objects.filter(Q(id_familiacargo=10) & Q(id_nivel=nivel_usuario.id_nivel) & Q(id_periodo=periodo_actual.id)).aggregate(
                Sum('dias_habiles')).values())[
            0]

        if auxiliares_horas is None:
            auxiliares_horas = 0
        else:
            auxiliares_horas= auxiliares_horas * 8


        jefe_departamento_count = Ges_Registro_Horas.objects.filter(Q(id_familiacargo=1) & Q(id_nivel=nivel_usuario.id_nivel) & Q(id_periodo=periodo_actual.id)).count()

        jefe_subdepartamento_count = Ges_Registro_Horas.objects.filter(Q(id_familiacargo=2) & Q(id_nivel=nivel_usuario.id_nivel) & Q(id_periodo=periodo_actual.id)).count()
        coordinadores_count= Ges_Registro_Horas.objects.filter(Q(id_familiacargo=3) & Q(id_nivel=nivel_usuario.id_nivel) & Q(id_periodo=periodo_actual.id)).count()
        supervisores_count =  Ges_Registro_Horas.objects.filter(Q(id_familiacargo=4) & Q(id_nivel=nivel_usuario.id_nivel) & Q(id_periodo=periodo_actual.id)).count()
        analistas_especialistar_count = Ges_Registro_Horas.objects.filter(Q(id_familiacargo=5) & Q(id_nivel=nivel_usuario.id_nivel) & Q(id_periodo=periodo_actual.id)).count()
        analistas_count = Ges_Registro_Horas.objects.filter(Q(id_familiacargo=6) & Q(id_nivel=nivel_usuario.id_nivel) & Q(id_periodo=periodo_actual.id)).count()
        supervisores_operativos_count = Ges_Registro_Horas.objects.filter(Q(id_familiacargo=7) & Q(id_nivel=nivel_usuario.id_nivel) & Q(id_periodo=periodo_actual.id)).count()
        operativos_count = Ges_Registro_Horas.objects.filter(Q(id_familiacargo=8) & Q(id_nivel=nivel_usuario.id_nivel) & Q(id_periodo=periodo_actual.id)).count()
        asistentes_count =  Ges_Registro_Horas.objects.filter(Q(id_familiacargo=9) & Q(id_nivel=nivel_usuario.id_nivel) & Q(id_periodo=periodo_actual.id)).count()
        auxiliares_count = Ges_Registro_Horas.objects.filter(Q(id_familiacargo=10) & Q(id_nivel=nivel_usuario.id_nivel) & Q(id_periodo=periodo_actual.id)).count()

        total_familia= Ges_Registro_Horas.objects.filter(Q(id_nivel=nivel_usuario.id_nivel) & Q(id_periodo=periodo_actual.id)).count()


        if dias_totales is None:
            horas_totales = 0
        else:
             horas_totales= dias_totales * 8

        context['object_list'] = lista_horas
        context['calculo'] = {'dias_totales': dias_totales ,
                              'horas_totales': horas_totales,
                              'jefe_departamento_totales':jefe_departamento_totales,
                              'jefe_subdepartamento_totales': jefe_subdepartamento_totales,
                              'coordinadores_totales':coordinadores_totales,
                              'supervisores_totales': supervisores_totales,
                              'analistas_especialistar_totales': analistas_especialistar_totales,
                              'analistas_totales': analistas_totales,
                              'supervisores_operativos_totales': supervisores_operativos_totales,
                              'operativos_totales': operativos_totales,
                              'asistentes_totales': asistentes_totales,
                              'auxiliares_totales': auxiliares_totales,
                              'jefe_departamento_horas': jefe_departamento_horas,
                              'jefe_subdepartamento_horas': jefe_subdepartamento_horas,
                              'coordinadores_horas': coordinadores_horas,
                              'supervisores_horas': supervisores_horas,
                              'analistas_especialistar_horas': analistas_especialistar_horas,
                              'analistas_horas': analistas_horas,
                              'supervisores_operativos_horas': supervisores_operativos_horas,
                              'operativos_horas': operativos_horas,
                              'asistentes_horas': asistentes_horas,
                              'auxiliares_horas': auxiliares_horas,
                              'jefe_departamento_count':jefe_departamento_count,
                              'jefe_subdepartamento_count': jefe_subdepartamento_count,
                              'coordinadores_count': coordinadores_count,
                              'supervisores_count': supervisores_count,
                              'analistas_especialistar_count': analistas_especialistar_count,
                              'analistas_count': analistas_count,
                              'supervisores_operativos_count': supervisores_operativos_count,
                              'operativos_count': operativos_count,
                              'asistentes_count': asistentes_count,
                              'auxiliares_count': auxiliares_count,
                              'total_familia':total_familia,


                              }

        return context



class RegistroHorasCreate(SuccessMessageMixin, CreateView ):
    form_class = GestionHorasForm
    template_name = 'registro_horas/registro_horas_form.html'


    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        id_usuario_actual = self.request.user.id  # obtiene id usuario actual
        id_usuario_ingreso= request.POST['id_user']

        try:
            periodo_actual = Glo_Periodos.objects.get(id_estado=1)
        except Glo_Periodos.DoesNotExist:
            return None



        # try:
        #     existe_usuario =  Ges_Registro_Horas.objects.get(Q(id_user=id_usuario_ingreso) & Q(id_periodo=periodo_actual.id))
        # except Ges_Registro_Horas.DoesNotExist:
        #     existe_usuario = None


        nivel_usuario =  Ges_Jefatura.objects.values('id_nivel').get(id_user=id_usuario_actual)['id_nivel']

        id_nivel =Ges_Niveles.objects.get(id=nivel_usuario)

        anio_hoy=date.today().year


        fecha_inicio = request.POST['fecha_inicio']
        fecha_termino = request.POST['fecha_termino']

        fecha_inicio_split = datetime.datetime.strptime(fecha_inicio, '%Y-%m-%d')
        fecha_termino_split = datetime.datetime.strptime(fecha_termino, '%Y-%m-%d')

        anio_inicio= fecha_inicio_split.year
        mes_inicio = fecha_inicio_split.month
        dia_inicio = fecha_inicio_split.day

        anio_termino= fecha_termino_split.year
        mes_termino = fecha_termino_split.month
        dia_termino = fecha_termino_split.day

        dias_habiles_brutos = workdays(datetime.datetime(anio_inicio, mes_inicio, dia_inicio),
                        datetime.datetime(anio_termino, mes_termino, dia_termino))


        if  request.POST['tiene_vacaciones'] == 'True':

            dias_habiles_brutos_vacaciones= len(dias_habiles_brutos) - 21 #se le restan las vacaciones y los administrativos
        else:
            dias_habiles_brutos_vacaciones = len(dias_habiles_brutos) - 6 #se le restan solo los administrativos



        feriados = Ges_Feriados.objects.filter(Q(id_periodo=periodo_actual.id) & Q(fecha_feriado__range =(fecha_inicio,fecha_termino))).count() #cuenta los feriados entre las fechas de inicio y termino.


        dias_habiles_brutos_vacaciones_feriados= dias_habiles_brutos_vacaciones - feriados

        if (anio_inicio == anio_hoy and anio_termino == anio_hoy) and (fecha_inicio < fecha_termino):
            if form.is_valid():
                if dias_habiles_brutos_vacaciones_feriados < 1:
                    request.session['message_class'] = "alert alert-warning"
                    messages.error(self.request,
                                   "Aviso :  El cálculo de días hábiles no puede ser menor a 1, revise la fecha de inicio y fecha de termino ingresada.")
                    return HttpResponseRedirect('/horas/listar/')
                else:

                    form.instance.id_nivel = id_nivel
                    form.instance.dias_habiles = dias_habiles_brutos_vacaciones_feriados
                    form.instance.id_periodo = periodo_actual
                    form.save()
                    request.session['message_class'] = "alert alert-success"
                    messages.success(self.request, "Los datos fueron creados correctamente!")
                    return HttpResponseRedirect('/horas/listar/')

            else:
                request.session['message_class'] = "alert alert-danger"
                messages.error(self.request, "Error interno: No se ha creado el registro. Comuníquese con el administrador.")
                return HttpResponseRedirect('/horas/listar/')
        else:
            request.session['message_class'] = "alert alert-warning"
            messages.error(self.request, "Aviso : El año ingresado debe ser el 2021 y los rangos válidos.")
            return HttpResponseRedirect('/horas/listar/')



class RegistroHorasDelete(SuccessMessageMixin, DeleteView ):
    model = Ges_Registro_Horas
    template_name = 'registro_horas/registro_horas_delete.html'

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        try:
            obj.delete()
            request.session['message_class'] = "alert alert-success"
            messages.success(self.request, "El registro fue eliminado correctamente!")
            return HttpResponseRedirect('/horas/listar/')

        except ProtectedError as e:
            request.session['message_class'] = "alert alert-warning"
            messages.error(request, "Aviso Integridad: Este nivel posee subniveles los que deben ser borrados antes de borrar este nivel.")
            return HttpResponseRedirect('/horas/listar/')

        except Exception  as e:
            request.session['message_class'] = "alert alert-danger"
            messages.error(request, "Error interno: No se ha eliminado el registro. Comuníquese con el administrador.")
            return HttpResponseRedirect('/horas/listar/')


class RegistroHorasUpdate(SuccessMessageMixin, UpdateView ):
    model = Ges_Registro_Horas
    form_class = GestionHorasUpdateForm
    template_name = 'registro_horas/registro_horas_update_form.html'


    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
       # form = self.get_form(form_class)
        id_nivel = kwargs['pk']
        instancia_nivel = self.model.objects.get(id=id_nivel)
        form = self.form_class(request.POST, instance=instancia_nivel)

        id_usuario_actual = self.request.user.id  # obtiene id usuario actual
        id_usuario_ingreso= request.POST['id_user']
        id_usuario_ingreso_int=int(id_usuario_ingreso)

        try:
            periodo_actual = Glo_Periodos.objects.get(id_estado=1)
        except Glo_Periodos.DoesNotExist:
            periodo_actual = None


        try:
            id_usuario_fila= Ges_Registro_Horas.objects.values('id_user').get(id=kwargs['pk'])[
                'id_user']
        except Ges_Registro_Horas.DoesNotExist:
            id_usuario_fila = None

        # try:
        #     existe_usuario =  Ges_Registro_Horas.objects.get(Q(id_user=id_usuario_ingreso) & Q(id_periodo=periodo_actual.id))
        # except Ges_Registro_Horas.DoesNotExist:
        #     existe_usuario = None

        nivel_usuario =  Ges_Jefatura.objects.values('id_nivel').get(id_user=id_usuario_actual)['id_nivel']
        id_nivel =Ges_Niveles.objects.get(id=nivel_usuario)

        anio_hoy=date.today().year


        fecha_inicio=request.POST['fecha_inicio']
        fecha_termino = request.POST['fecha_termino']


        fecha_inicio_split = datetime.datetime.strptime(fecha_inicio, '%Y-%m-%d')
        fecha_termino_split = datetime.datetime.strptime(fecha_termino, '%Y-%m-%d')

        anio_inicio= fecha_inicio_split.year
        mes_inicio = fecha_inicio_split.month
        dia_inicio = fecha_inicio_split.day

        anio_termino= fecha_termino_split.year
        mes_termino = fecha_termino_split.month
        dia_termino = fecha_termino_split.day

        dias_habiles_brutos = workdays(datetime.datetime(anio_inicio, mes_inicio, dia_inicio),
                        datetime.datetime(anio_termino, mes_termino, dia_termino))


        if  request.POST['tiene_vacaciones'] == 'True':

            dias_habiles_brutos_vacaciones= len(dias_habiles_brutos) - 21 #se le restan las vacaciones y los administrativos
        else:
            dias_habiles_brutos_vacaciones = len(dias_habiles_brutos) - 6 #se le restan solo los administrativos





        feriados = Ges_Feriados.objects.filter(Q(id_periodo=periodo_actual.id) & Q(fecha_feriado__range =(fecha_inicio,fecha_termino))).count() #cuenta los feriados entre las fechas de inicio y termino.

        dias_habiles_brutos_vacaciones_feriados= dias_habiles_brutos_vacaciones - feriados

        if   (anio_inicio == anio_hoy and anio_termino == anio_hoy) and (fecha_inicio<fecha_termino):
            if form.is_valid():
                if dias_habiles_brutos_vacaciones_feriados < 1:
                    request.session['message_class'] = "alert alert-warning"
                    messages.error(self.request,
                                   "Aviso :  El cálculo de días hábiles no puede ser menor a 1, revise la fecha de inicio y fecha de termino ingresada.")
                    return HttpResponseRedirect('/horas/listar/')
                else:

                    form.instance.id_nivel = id_nivel
                    form.instance.dias_habiles = dias_habiles_brutos_vacaciones_feriados
                    form.instance.id_periodo = periodo_actual
                    form.save()
                    request.session['message_class'] = "alert alert-success"
                    messages.success(self.request, "Los datos fueron creados correctamente!")
                    return HttpResponseRedirect('/horas/listar/')

            else:
                request.session['message_class'] = "alert alert-danger"
                messages.error(self.request, "Error interno: No se ha creado el registro. Comuníquese con el administrador.")
                return HttpResponseRedirect('/horas/listar/')
        else:
            request.session['message_class'] = "alert alert-warning"
            messages.error(self.request, "Aviso : El año ingresado debe ser el 2021 y los rangos válidos.")
            return HttpResponseRedirect('/horas/listar/')

        # if   (anio_inicio == anio_hoy and anio_termino == anio_hoy) and (fecha_inicio<fecha_termino):
        #     if form.is_valid():
        #         if existe_usuario and (id_usuario_fila != id_usuario_ingreso_int):
        #             request.session['message_class'] = "alert alert-warning"
        #             messages.error(self.request,
        #                            "Aviso :  El usuario ya se encuentra ingresado en "  + str(existe_usuario.id_nivel) +  ", vuelva a intentarlo.")
        #             return HttpResponseRedirect('/horas/listar/')
        #         else:
        #             if dias_habiles_brutos_vacaciones_feriados < 1:
        #
        #                 request.session['message_class'] = "alert alert-warning"
        #                 messages.error(self.request,
        #                                "Aviso :  El cálculo de días hábiles no puede ser menor a 1, revise la fecha de inicio y fecha de termino ingresada.")
        #                 return HttpResponseRedirect('/horas/listar/')
        #             else:
        #
        #                 form.instance.id_nivel = id_nivel
        #                 form.instance.dias_habiles = dias_habiles_brutos_vacaciones_feriados
        #
        #                 form.save()
        #                 request.session['message_class'] = "alert alert-success"
        #                 messages.success(self.request, "Los datos fueron actualizados correctamente!")
        #                 return HttpResponseRedirect('/horas/listar/')
        #     else:
        #
        #
        #         request.session['message_class'] = "alert alert-danger"
        #         messages.error(self.request, "Error interno: No se ha actualizado el registro. Comuníquese con el administrador.")
        #         return HttpResponseRedirect('/horas/listar/')
        # else:
        #     request.session['message_class'] = "alert alert-warning"
        #     messages.error(self.request, "Aviso: El año ingresado debe ser el presente y los rangos válidos.")
        #     return HttpResponseRedirect('/horas/listar/')

