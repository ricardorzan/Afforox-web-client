from django.db import models

# Create your models here.

class Usuario(models.Model):
    nombre_completo = models.CharField(max_length=200)
    correo_electrónico = models.CharField(max_length=200)
    fecha_de_nacimiento = models.DateField()
    edad = models.CharField(max_length=20)
    número_de_télefono = models.CharField(max_length=20)
    contraseña = models.CharField(max_length=50)

class Pais(models.Model):
    país = models.CharField(max_length=20)

class Estado(models.Model):
    estado = models.CharField(max_length=20)
    país = models.ForeignKey(Pais, on_delete=models.CASCADE)

class Ciudad(models.Model):
    ciudad = models.CharField(max_length=20)
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE)

class Domicilio(models.Model):
    país = models.CharField(max_length=20)
    estado = models.CharField(max_length=20)
    ciudad = models.CharField(max_length=20)
    calle = models.CharField(max_length=20)
    número_interior = models.CharField(max_length=20)
    número_exterior = models.CharField(max_length=20)
    colonia = models.CharField(max_length=20)