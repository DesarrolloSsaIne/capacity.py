from django.shortcuts import render
from django.views.generic import ListView
# Create your views here.
from apps.jefaturas.models import Ges_Jefatura
from apps.estructura.models import Ges_Niveles
from django.db.models import Q
from django.db.models import Case, CharField, Value, When

from apps.objetivos.models import Ges_Objetivo_Estrategico, Ges_Objetivo_Operativo, Ges_Objetivo_Tactico, Ges_Objetivo_TacticoTN


class ObjetivosEstrategicosList(ListView):
    model= Ges_Objetivo_Operativo
    template_name = "vista_objetivos/vista_objetivos_listar.html"

    def get_context_data(self,  **kwargs,):
        context = super(ObjetivosEstrategicosList, self).get_context_data(**kwargs)
        id_usuario_actual= self.request.user.id #obtiene id usuario actual
        try:
            nivel_usuario= Ges_Jefatura.objects.get(id_user=id_usuario_actual)
        except Ges_Jefatura.DoesNotExist:
            context['habilitado'] = {'mensaje': False}
            return None
        id_nivel =nivel_usuario.id_nivel.id
        replies = Ges_Niveles.objects.filter(id=id_nivel).annotate(
            nivel_order=Case(
                When(orden_nivel=1, then='id_primer_nivel'),
                When(orden_nivel=2, then='id_segundo_nivel'),
                When(orden_nivel=3, then='id_tercer_nivel'),
                When(orden_nivel=4, then='id_cuarto_nivel'),
               output_field=CharField(),
            )
        )
        for nivel in replies:
            id_nivel_final = nivel.nivel_order
            id_orden = nivel.orden_nivel

        if  id_orden == 1:
            replies2 = Ges_Objetivo_Operativo.objects.all().filter(id_objetivo_tacticotn__id_objetivo_tactico__id_objetivo_estrategico__ges_primer_nivel__id=id_nivel_final, transversal = False)
        if id_orden == 2:
            replies2 = Ges_Objetivo_Tactico.objects.filter(id_segundo_nivel=id_nivel_final, transversal = False)
        if  id_orden ==3:
            replies2 = Ges_Objetivo_TacticoTN.objects.filter(id_tercer_nivel=id_nivel_final, transversal = False)
        if  id_orden == 4:
            replies2 = Ges_Objetivo_Operativo.objects.filter(id_cuarto_nivel=id_nivel_final, transversal = False)

        context['niveles'] = replies2
        context['orden'] = {'orden_nivel': id_orden }
        return context




