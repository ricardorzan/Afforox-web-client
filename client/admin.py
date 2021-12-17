from django.contrib import admin
from .models import (
    Usuario,
    Domicilio, Sucursal, Negocio
)

# Register your models here.
admin.site.register(Usuario)
admin.site.register(Sucursal)
admin.site.register(Negocio)
admin.site.register(Domicilio)
