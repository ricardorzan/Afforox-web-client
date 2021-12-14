from django.db import models
from django.utils.translation import ugettext_lazy as _

# Create your models here.
from multiselectfield import MultiSelectField


class Sesion:
    token = ''


class Domicilio(models.Model):
    calle = models.CharField('Calle', max_length=20)
    ciudad = models.CharField('Ciudad', max_length=20)
    colonia = models.CharField('Colonia', max_length=20)
    estado = models.CharField('Estado', max_length=20)
    municipio = models.CharField('Municipio', max_length=20)
    numero_exterior = models.CharField('Número exterior', max_length=20)
    numero_interior = models.CharField('Número interior', max_length=20)
    pais = models.CharField('País', max_length=20)
    id = models.AutoField('ID', primary_key=True)


class Usuario(models.Model):
    contrasenia = models.CharField('Contraseña', max_length=50)
    correo_electronico = models.CharField('Correo electrónico', max_length=200, primary_key=True)
    edad = models.CharField('Edad', max_length=20)
    fecha_de_nacimiento = models.DateField('Fecha de nacimiento', )
    foto_de_perfil = models.ImageField('Foto de perfil', upload_to='profile_pictures', blank=True)
    nombre_completo = models.CharField('Nombre completo', max_length=200)
    telefono = models.CharField('Telefono', max_length=20)
    codigo_autenticacion = models.CharField('Código de autenticación', max_length=200)


TIPO = [
    ('RESTAURANTE', 'Restaurante'),
    ('ESTETICA', 'Estética'),
    ('SALONBELLEZA', 'Salón de belleza'),
    ('BARBERIA', 'Barberia'),
    ('GIMNASIO', 'Gimnasio'),
    ('Otro', 'Otro'),
]


class Negocio(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    facebook = models.CharField('Facebook', max_length=100)
    fotoPerfil = models.ImageField('Foto de perfil', upload_to='profile_pictures', blank=True)
    instagram = models.CharField('Instagram', max_length=100)
    nombreCompleto = models.CharField('Nombre', max_length=20)
    telefono = models.CharField('Telefono', max_length=20)
    whatsapp = models.CharField('WhatsApp', max_length=20)
    negocioid = models.AutoField(primary_key=True)
    tipoNegocio = models.CharField('Tipo de negocio', max_length=20)
    correoElectronico = models.CharField('Correo electrónico', max_length=200)


MEDIDAS = [
    ('SANADISTANCIA', 'Sana distancia entre clientes'),
    ('TOMADETEMPERATURA', 'Toma de temperatura a trabajadores y clientes'),
    ('TRABAJADORESCONPROTECCION', 'Equipo de protección a trabajadores'),
    ('GELDESINFECTANTE', 'Aplicación de gel desinfectante'),
    ('CUBREBOCASOBLIGATORIO', 'Uso obligatorio de cubrebocas a clientes'),
    ('AGUAYJABONENBAÑOS', 'Sanitarios con agua y jabón'),
    ('DESINFECCIONDESUPERFICIES', 'Desinfección de superficies'),
    ('ENTRADASYSALIDASSEPARADAS', 'Entrada y salidas separadas'),
    ('SANITIZACIONDELESTABLECIMIENTO', 'Sanitización del establecimiento'),
    ('SANADISTANCIAMARCADAENFILAS', 'Sana distancia marcada para las filas'),
    ('OTRA', 'Otra')
]

SERVICIOS = [
    ('ESTACIONAMIENTO', 'Estacionamiento'),
    ('VALETPARKING', 'Servicio de valet parking'),
    ('AREAINFANTIL', 'Área infantil'),
    ('DELIVERY', 'Entrega a domicilio'),
    ('PARALLEVAR', 'Servicio para llevar'),
    ('AREAAIRELIBRE', 'Área al aire libre'),
    ('WIFI', 'Conexión WiFi'),
    ('RESERVACIONES', 'Reservaciones')
]


class Sucursal(models.Model):
    aforo_actual = models.CharField('Aforo actual', max_length=20)
    aforo_total = models.CharField('Aforo total', max_length=20)
    nombre_sucursal = models.CharField('Nombre de la sucursal', max_length=20)
    telefono = models.CharField('Telefono', max_length=20)
    sucursalid = models.AutoField(primary_key=True)
    domicilioid = models.ForeignKey(Domicilio, on_delete=models.CASCADE)
    negocioid = models.ForeignKey(Negocio, on_delete=models.CASCADE)
    medidas = MultiSelectField(choices=MEDIDAS, blank=True)
    servicios = MultiSelectField(choices=SERVICIOS, blank=True)


class Dia(models.TextChoices):
    LUNES = 'LUNES', _('Lunes')
    MARTES = 'MARTES', _('Martes')
    MIERCOLES = 'MIERCOLES', _('Miercoles')
    JUEVES = 'JUEVES', _('Jueves')
    VIERNES = 'VIERNES', _('Viernes')
    SABADO = 'SABADO', _('Sabado')
    DOMINGO = 'DOMINGO', _('Domingo')
    TODOS = 'TODOS', _('Todos')


class Horario(models.Model):
    horario_apertura = models.TimeField('Horario apertura')
    horario_cierre = models.TimeField('Horario cierre')
    dia = models.CharField(max_length=12, choices=Dia.choices, default=Dia.TODOS, blank=True)
    sucursalid = models.ForeignKey(Sucursal, on_delete=models.CASCADE)
    horarioid = models.AutoField(primary_key=True)
