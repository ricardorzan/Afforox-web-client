import json

import requests
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.decorators.http import condition
from django.views.generic import ListView
from django.views.generic.edit import CreateView, FormView
from .models import Usuario, Domicilio, Negocio, Sucursal, Sesion
from .forms import (
    LogInForm,
    AuthForm,
    MainForm,
    BusinessForm,
    SucursalForm,
    DomicilioForm,
    HorarioGeneralForm,
    UsuarioForm
)

# Create your views here.
from django.views import View

from .serializers import BusinessSerializer, UserSerializer


class Homepage(View):
    template_name = "home.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        return render(request, self.template_name)


def About(request):
    return render(request, "about.html")


class LogInView(FormView):
    form_class = LogInForm
    template_name = "login.html"
    isAuthenticated = False

    def form_valid(self, form):
        try:
            response = form.login()
            if response.status_code == 200:
                Sesion.token = response.text
                Sesion.username = form.cleaned_data.get('correo_electronico')
                self.isAuthenticated = True
                return HttpResponseRedirect(self.get_success_url())
            elif response.status_code == 401:
                return HttpResponseRedirect(self.get_success_url(username=form.cleaned_data.get('correo_electronico')))
            elif response.status_code == 403:
                messages.error(self.request, 'Contraseña erronea')
                return self.form_invalid(form)
            elif response.status_code == 404:
                messages.error(self.request, 'No se ha encontrado un usuario con el correo electronico')
                return self.form_invalid(form)
        except:
            messages.error(self.request, 'Error en el servidor, intente más tarde')
            return self.form_invalid(form)

    def form_invalid(self, form):
        response = super().form_invalid(form)
        if self.request.accepts('text/html'):
            return response
        else:
            return JsonResponse(form.errors, status=400)

    def get_success_url(self, **kwargs):
        if not self.isAuthenticated:
            return reverse_lazy('auth', kwargs={'username': kwargs['username']})
        else:
            return reverse_lazy('main')


class AccountCreateView(View):
    template_name = "signup.html"
    usuario_form = UsuarioForm
    domicilio_form = DomicilioForm
    context = {}
    context['usuario_form'] = usuario_form(prefix='usuario')
    context['domicilio_form'] = domicilio_form(prefix='domicilio')

    def get(self, request):
        return render(request, self.template_name, self.context)

    def post(self, request):
        usuario_form = UsuarioForm(request.POST, request.FILES, prefix='usuario')
        if usuario_form.is_valid():
            domicilio_form = DomicilioForm(request.POST, prefix='domicilio')
            if domicilio_form.is_valid():
                response = UserSerializer.register_user(usuario_form.cleaned_data, domicilio_form.cleaned_data)
                if response.status_code == 201:
                    messages.success(self.request, 'Tu negocio ha sido registrado correctamente',
                                     extra_tags='alert alert-success')
                    return HttpResponseRedirect(
                        self.get_success_url(username=usuario_form.cleaned_data.get('correo_electronico')))
                else:
                    messages.error(self.request, 'Error al registrar', extra_tags='alert alert-danger')
                    return render(request, self.template_name, self.context)
            else:
                messages.warning(self.request, 'Error en el formulario domicilio', extra_tags='alert alert-warning')
                messages.warning(self.request, domicilio_form.errors, extra_tags='alert alert-warning')
                return render(request, self.template_name, self.context)
        else:
            print(usuario_form.errors)
            messages.warning(self.request, 'Error en el formulario usuario', extra_tags='alert alert-warning')
            messages.warning(self.request, usuario_form.errors, extra_tags='alert alert-warning')
            return render(request, self.template_name, self.context)

    def get_success_url(self, **kwargs):
        return reverse_lazy('auth', kwargs={'username': kwargs['username']})


class AuthView(FormView):
    form_class = AuthForm
    template_name = "auth.html"
    success_url = '/'

    def form_valid(self, form):
        response = form.auth(self.kwargs['username'])
        if response.status_code == 200:
            messages.success(self.request, 'Tu cuenta ha sido autenticada con éxito, prueba iniciar sesión',
                             extra_tags='alert alert-success')
            return HttpResponseRedirect(self.request.path)
        elif response.status_code == 403:
            messages.warning(self.request,
                             'El estado de su usuario es diferente a no autenticado. Si no puede iniciar sesión '
                             'probablemente el estado de su cuenta ha cambiado a suspendido por normas de los '
                             'moderadores.', extra_tags='alert alert-warning')
            return self.form_invalid(form)
        elif response.status_code == 401:
            messages.error(self.request, 'Codigo de autenticación erroneo', extra_tags='alert alert-danger')
            return self.form_invalid(form)
        elif response.status_code == 404:
            messages.error(self.request, 'No se ha encontrado un usuario con el correo electronico',
                           extra_tags='alert alert-danger')
            return self.form_invalid(form)

    def form_invalid(self, form):
        response = super().form_invalid(form)
        if self.request.accepts('text/html'):
            return response
        else:
            return JsonResponse(form.errors, status=400)


class MainMenuView(View):
    template_name = "main.html"
    main_form = MainForm
    context = {}
    context['main_form'] = main_form

    def get(self, request):
        response = self.context['main_form'].get_data(self, 0, 20)
        self.context['object_list'] = json.loads(response.content.decode('utf-8'))
        return render(request, self.template_name, self.context)

    def post(self):
        pass


class RegisterBusiness(View):
    template_name = "register_business.html"
    negocio_form = BusinessForm
    sucursal_form = SucursalForm
    domicilio_form = DomicilioForm
    horario_form = HorarioGeneralForm
    context = {}
    context['negocio_form'] = negocio_form(prefix='negocio')
    context['sucursal_form'] = sucursal_form(prefix='sucursal')
    context['domicilio_form'] = domicilio_form(prefix='domicilio')
    context['horario_form'] = horario_form(prefix='horario')

    def get(self, request):
        return render(request, self.template_name, self.context)

    def post(self, request):
        negocio_form = BusinessForm(request.POST, request.FILES, prefix='negocio')
        if negocio_form.is_valid():
            sucursal_form = SucursalForm(request.POST, prefix='sucursal')
            if sucursal_form.is_valid():
                domicilio_form = DomicilioForm(request.POST, prefix='domicilio')
                if domicilio_form.is_valid():
                    horario_form = HorarioGeneralForm(request.POST, prefix='horario')
                    if horario_form.is_valid():
                        response = BusinessSerializer.register_business(negocio_form.cleaned_data,
                                                                        sucursal_form.cleaned_data,
                                                                        domicilio_form.cleaned_data,
                                                                        horario_form.cleaned_data)
                        if response.status_code == 201:
                            messages.success(self.request, 'Tu negocio ha sido registrado correctamente',
                                             extra_tags='alert alert-success')
                            return HttpResponseRedirect(self.get_success_url())
                        else:
                            messages.error(self.request, 'Error al registrar', extra_tags='alert alert-danger')
                            return self.form_invalid()
                    else:
                        messages.warning(self.request, 'Error en el formulario negocio',
                                         extra_tags='alert alert-warning')
                        return self.form_invalid()
                else:
                    messages.warning(self.request, 'Error en el formulario domicilio', extra_tags='alert alert-warning')
                    return self.form_invalid()
            else:
                messages.warning(self.request, 'Error en el formulario sucursal', extra_tags='alert alert-warning')
                return self.form_invalid()
        else:
            messages.warning(self.request, 'Error en el formulario negocio', extra_tags='alert alert-warning')
            return self.form_invalid()

    def get_success_url(self):
        return reverse_lazy('main')
