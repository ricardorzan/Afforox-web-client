from django import forms
from django.utils.translation import ugettext_lazy as _
from .models import (
    Usuario,
    Domicilio
)

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
        error_messages = {
            'nombre_completo': {
                'required': _('Este campo es requerido')
            },
            'correo_electrónico': {
                'required': _('Este campo es requerido')
            },
            'fecha_de_nacimiento': {
                'required': _('Este campo es requerido')
            },
            'edad': {
                'required': _('Este campo es requerido')
            },
            'número_de_télefono': {
                'required': _('Este campo es requerido')
            },
            'contraseña': {
                'required': _('Este campo es requerido')
            },
            'foto_de_perfil': {
                'required': _('Este campo es requerido')
            }
        }

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
            'número_interior':  forms.TextInput(attrs={'class': 'form-control'})
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