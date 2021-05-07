from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth import authenticate
from django.http import HttpResponseRedirect
from django.contrib import auth
from apps.registration.models import logAcceso
from django.views.generic import ListView

def login(request):

    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)

        if form.is_valid():

            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            userlog = User.objects.get(username=username)
            nombre = userlog.get_full_name()

            if user is not None:
                if userlog in User.objects.filter(groups__in=Group.objects.all()):

                    CreateLogAcceso(username, nombre)
                    auth.login(request, user)

                    return HttpResponseRedirect('/dashboard')

                else:
                    messages.error(request, "Usuario no válido para este sistema.")
            else:
                messages.error(request, "Usuario o Password Incorrectas.")
        else:
            messages.error(request, "Usuario o Password Incorrectas")
    form = AuthenticationForm()
    return render(request=request, template_name="registration/login.html", context={"form": form})

def logout(request):
    #del request.session['grupo']
    auth.logout(request)
    return HttpResponseRedirect('/accounts/login')



def CreateLogAcceso(usr, nombre):

    logAcceso.objects.create(
        user=usr,
        nombre=nombre,

    )
    return None

class LogList(ListView):
    model = logAcceso
    template_name = 'registration/log_list.html'


    def get_context_data(self,  **kwargs):
        context = super(LogList, self).get_context_data(**kwargs)
        lista_log= logAcceso.objects.all().order_by('-id')
        context['object_list'] = lista_log
        return context


