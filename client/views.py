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
    LogInForm, SignUpForm, AuthForm, MainForm, BusinessForm, SucursalForm, DomicilioForm, HorarioGeneralForm
)

# Create your views here.
from django.views import View


def Homepage(request):
    return render(request, "home.html")


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


class AccountCreateView(FormView):
    form_class = SignUpForm
    template_name = "signup.html"
    success_url = '/auth/'

    def form_valid(self, form):
        response = form.signup()
        if response.status_code == 201:
            return HttpResponseRedirect(self.get_success_url(username=form.cleaned_data.get('correoElectronico')))
            return self.form_invalid(form)
        elif response.status_code == 404:
            messages.error(self.request, 'Ya hay una cuenta registrada con el correo electronico')
            return self.form_invalid(form)

    def form_invalid(self, form):
        response = super().form_invalid(form)
        if self.request.accepts('text/html'):
            return response
        else:
            return JsonResponse(form.errors, status=400)

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
            messages.error(self.request, 'No se ha encontrado un usuario con el correo electronico')
            return self.form_invalid(form)

    def form_invalid(self, form):
        response = super().form_invalid(form)
        if self.request.accepts('text/html'):
            return response
        else:
            return JsonResponse(form.errors, status=400)


class MainMenuView(ListView):
    template_name = "main.html"
    model = Negocio

    def get(self, request):
        response = MainForm.get_data(self, 0, 20)
        return render(request, self.template_name)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context


class RegisterBusiness(View):
    template_name = "register_business.html"
    negocio_form = BusinessForm
    sucursal_form = SucursalForm
    domicilio_form = DomicilioForm
    horario_form = HorarioGeneralForm

    def get(self, request):
        context = {}
        context['negocio_form'] = self.negocio_form(prefix='negocio')
        context['sucursal_form'] = self.sucursal_form(prefix='sucursal')
        context['domicilio_form'] = self.domicilio_form(prefix='domicilio')
        context['horario_form'] = self.horario_form(prefix='horario')
        return render(request, self.template_name, context)

    def post(self, request):
        negocio_form = BusinessForm(request.POST, prefix='negocio')
        if negocio_form.is_valid():
            sucursal_form = SucursalForm(request.POST, prefix='sucursal')
            if sucursal_form.is_valid():
                horario_form = HorarioGeneralForm(request.POST, prefix='horario')
                if horario_form.is_valid():
                    BusinessForm.register_business(sucursal_form, horario_form)
                else:
                    print(horario_form.errors)


