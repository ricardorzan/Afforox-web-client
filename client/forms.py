import json

import requests
from django import forms
from django.http import JsonResponse
from django.utils.translation import ugettext_lazy as _
from multiselectfield import MultiSelectField

from .models import (
    Usuario,
    Domicilio, Negocio, Sucursal, Horario, TIPO,
)

API_URL = 'http://127.0.0.8:8080/Afforox'


class DateInput(forms.DateInput):
    input_type = 'date'


class LogInForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['correo_electronico', 'contrasenia']
        widgets = {
            'correo_electronico': forms.EmailInput(attrs={'class': 'form-control'}),
            'contrasenia': forms.PasswordInput(attrs={'class': 'form-control'})
        }
        error_messages = {
            'correo_electronico': {
                'required': _('Este campo es requerido')
            },
            'contrasenia': {
                'required': _('Este campo es requerido')
            }
        }

    def login(self):
        data = self.cleaned_data
        response = requests.post(
            API_URL + '/usuarios/login' + '?username=' + data['correo_electronico'] + '&password=' + data[
                'contrasenia'],
            data=json.dumps(data, indent=4, sort_keys=True, default=str),
            headers={'Content-Type': 'application/json'})
        return response


class AuthForm(forms.Form):
    codigoAutenticacion = forms.CharField(label='Código de autenticación',
                                          widget=forms.TextInput(attrs={'class': 'form-control'}))

    def auth(self, username):
        data = self.cleaned_data
        response = requests.patch(
            API_URL + '/usuarios/validacion' + '?username=' + username + '&token=' + data['codigoAutenticacion'],
            data=json.dumps(data, indent=4, sort_keys=True, default=str),
            headers={'Content-Type': 'application/json'})
        return response


class MainForm(forms.Form):
    search = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Negocios'}))

    def get_data(self, salto, limite):
        response = None
        try:
            response = requests.get(
            API_URL + '/negocios' + '?salto=' + str(salto) + '&limite=' + str(limite),
            headers={'Content-Type': 'application/json'})
        except Exception:
            pass
        return response


class BusinessForm(forms.ModelForm):
    class Meta:
        model = Negocio
        exclude = ['usuario']
        widgets = {
            'correoElectronico': forms.EmailInput(attrs={'class': 'form-control'}),
            'nombreCompleto': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'pattern': '[0-9]+'}),
            'whatsapp': forms.TextInput(attrs={'class': 'form-control border-start-0', 'pattern': '[0-9]+'}),
            'facebook': forms.TextInput(attrs={'class': 'form-control border-start-0'}),
            'instagram': forms.TextInput(attrs={'class': 'form-control border-start-0'}),
            'tipoNegocio': forms.Select(choices=TIPO, attrs={'class': 'form-control', 'required': 'true'})
        }


class SucursalForm(forms.ModelForm):
    class Meta:
        model = Sucursal
        exclude = ['negocioid', 'domicilioid', 'aforo_actual']
        widgets = {
            'nombre_sucursal': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'pattern': '[0-9]+'}),
            'aforo_total': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'type': 'number'})
        }


class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        exclude = ['codigo_autenticacion']
        widgets = {
            'nombre_completo': forms.TextInput(attrs={'class': 'form-control'}),
            'correo_electronico': forms.EmailInput(attrs={'class': 'form-control'}),
            'fecha_de_nacimiento': DateInput(attrs={'class': 'form-control'}),
            'edad': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'pattern': '[0-9]+'}),
            'contrasenia': forms.PasswordInput(attrs={'class': 'form-control'})
        }


class DomicilioForm(forms.ModelForm):
    class Meta:
        model = Domicilio
        exclude = []
        widgets = {
            'pais': forms.Select(attrs={'class': 'form-control', 'required': 'true'}),
            'estado': forms.Select(attrs={'class': 'form-control', 'required': 'true'}),
            'ciudad': forms.Select(attrs={'class': 'form-control', 'required': 'true'}),
            'calle': forms.TextInput(attrs={'class': 'form-control'}),
            'colonia': forms.TextInput(attrs={'class': 'form-control'}),
            'numero_interior': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'numero_exterior': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'municipio': forms.TextInput(attrs={'class': 'form-control'})
        }


class HorarioGeneralForm(forms.ModelForm):
    class Meta:
        model = Horario
        exclude = ['sucursalid']
        widgets = {
            'horario_apertura': forms.TimeInput(attrs={'class': 'form-control', 'required': 'true', 'type': 'time'}),
            'horario_cierre': forms.TimeInput(attrs={'class': 'form-control', 'required': 'true', 'type': 'time'}),
            'dia': forms.Select(attrs={'class': 'form-control', 'required': 'true', 'disabled': 'false'}),
        }
