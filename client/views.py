import json

import requests
from django.contrib import messages
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.views.decorators.http import condition
from django.views.generic.edit import CreateView, FormView
from .models import Usuario, Domicilio
from .forms import (
    LogInForm,
    SignUpUserForm,
    SignUpAddressForm, SignUpForm, AuthForm
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
    success_url = '/main/'

    def form_valid(self, form):
        form.login()
        return super().form_valid(form)


class AccountCreateView(FormView):
    form_class = SignUpForm
    template_name = "signup.html"
    success_url = '/auth/'

    def form_valid(self, form):
        response = form.login()
        if response.status_code == 200:
            return HttpResponseRedirect(self.get_success_url())
        elif response.status_code == 201:
            messages.error(self.request, 'La pura prueba mi pana')
            return self.form_invalid(form)

    def form_invalid(self, form):
        response = super().form_invalid(form)
        if self.request.accepts('text/html'):
            return response
        else:
            return JsonResponse(form.errors, status=400)


class AuthView(FormView):
    form_class = AuthForm
    template_name = "auth.html"
    success_url = '#'

    def form_valid(self, form):
        response = form.auth()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        pass



class MainMenuView(View):
    template_name = "main.html"

    def get(self, request):
        return render(request, self.template_name)
