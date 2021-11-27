import json

import requests
from django import forms
from django.http import JsonResponse
from django.utils.translation import ugettext_lazy as _
from .models import (
    Usuario,
    Domicilio
)

API_URL = 'http://192.168.100.8:8080/Afforox'


class DateInput(forms.DateInput):
    input_type = 'date'


class LogInForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['correo_electrónico', 'contraseña']
        labels = {
            'correo_electrónico': _('Correo electrónico:'),
            'contraseña': _('Contraseña:')
        }
        widgets = {
            'correo_electrónico': forms.EmailInput(attrs={'class': 'form-control'}),
            'contraseña': forms.PasswordInput(attrs={'class': 'form-control'})
        }
        error_messages = {
            'correo_electrónico': {
                'required': _('Este campo es requerido')
            },
            'contraseña': {
                'required': _('Este campo es requerido')
            }
        }

    def login(self):
        pass


class SignUpForm(forms.Form):
    nombreCompleto = forms.CharField(label='Nombre completo', widget=forms.TextInput(attrs={'class': 'form-control'}))
    correoElectronico = forms.EmailField(label='Correo electrónico',
                                         widget=forms.EmailInput(attrs={'class': 'form-control'}))
    fechaNacimiento = forms.CharField(label='Fecha de nacimiento', widget=DateInput(attrs={'class': 'form-control'}))
    edad = forms.CharField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    telefono = forms.CharField(label='Télefono',
                               widget=forms.TextInput(attrs={'class': 'form-control', 'pattern': '[0-9]+'}))
    pais = forms.CharField(label='País', widget=forms.Select(attrs={'class': 'form-control', 'required': 'true'}))
    estado = forms.CharField(widget=forms.Select(attrs={'class': 'form-control', 'required': 'true'}))
    ciudad = forms.CharField(widget=forms.Select(attrs={'class': 'form-control', 'required': 'true'}))
    calle = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    colonia = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    numeroInterior = forms.CharField(label='Número interior', widget=forms.NumberInput(attrs={'class': 'form-control'}))
    numeroExterior = forms.CharField(label='Número exterior', widget=forms.NumberInput(attrs={'class': 'form-control'}))
    contrasenia = forms.CharField(label='Contraseña', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def login(self):
        data = self.cleaned_data
        response = requests.post(API_URL + '/usuarios', data=json.dumps(data, indent=4, sort_keys=True, default=str),
                              headers={'Content-Type': 'application/json'})
        return response


class AuthForm(forms.Form):
    codigoAutenticacion = forms.CharField(label='Código de autenticación',
                                          widget=forms.TextInput(attrs={'class': 'form-control'}))

    def auth(self):
        data = self.cleaned_data
        r = requests.post(API_URL + '/usuarios/validadcion',
                          data=json.dumps(data, indent=4, sort_keys=True, default=str),
                          headers={'Content-Type': 'application/json'})
        return JsonResponse({}, status=200)


class SignUpUserForm(forms.ModelForm):
    class Meta:
        model = Usuario
        exclude = []
        widgets = {
            'nombre_completo': forms.TextInput(attrs={'class': 'form-control'}),
            'correo_electrónico': forms.EmailInput(attrs={'class': 'form-control'}),
            'fecha_de_nacimiento': DateInput(attrs={'class': 'form-control'}),
            'edad': forms.TextInput(attrs={'class': 'form-control'}),
            'número_de_télefono': forms.TextInput(attrs={'class': 'form-control'}),
            'contraseña': forms.PasswordInput(attrs={'class': 'form-control'}),
            'foto_de_perfil': forms.FileInput(attrs={'class': 'form-control'})
        }

    def signup(self):
        pass


class SignUpAddressForm(forms.ModelForm):
    class Meta:
        model = Domicilio
        exclude = []
        widgets = {
            'calle': forms.TextInput(attrs={'class': 'form-control'}),
            'país': forms.Select(attrs={'class': 'form-control'}),
            'ciudad': forms.Select(attrs={'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
            'colonia': forms.TextInput(attrs={'class': 'form-control'}),
            'número_exterior': forms.TextInput(attrs={'class': 'form-control'}),
            'número_interior': forms.TextInput(attrs={'class': 'form-control'})
        }
        error_messages = {
            'calle': {
                'required': _('Este campo es requerido')
            },
            'país': {
                'required': _('Este campo es requerido')
            },
            'ciudad': {
                'required': _('Este campo es requerido')
            },
            'estado': {
                'required': _('Este campo es requerido')
            },
            'colonia': {
                'required': _('Este campo es requerido')
            },
            'número_interior': {
                'required': _('Este campo es requerido')
            },
            'número_exterior': {
                'required': _('Este campo es requerido')
            }
        }
