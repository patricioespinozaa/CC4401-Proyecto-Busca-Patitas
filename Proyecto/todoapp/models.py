from django.db import models

# Create your models here.
from django.utils import timezone
from categorias.models import Categoria
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User

# Tareas
owner = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)

# Clase Usuario:
# Contiene email, celular, ubicacion y contraseña
class User(AbstractUser):
    email = models.EmailField(unique=True)
    celular = models.CharField(max_length=15, blank=True, null=True)  # Campo para celular
    ubicacion_personal = models.CharField(max_length=100, blank=True, null=True)  # Campo para ubicación personal
    contraseña = models.CharField(max_length=100, blank=True, null=True)  # Campo para contraseña

class Region(models.Model):
    #nombre de la region
    region = models.CharField(max_length=100)
    def __str__(self):
        return self.region


class Comuna(models.Model):
    #Nombre de la region
    region = models.ManyToManyField('Region')

    #Comuna
    comuna = models.CharField(max_length=100)

    def __str__(self):
        return self.comuna

# Modelo para representar una Mascota
class Mascota(models.Model):
    # Nombre de la mascota
    nombre = models.CharField(max_length=100)
    # Fecha en que se extravió la mascota
    fecha_extravio = models.DateField()
    # Hora en que se extravió la mascota
    hora_extravio = models.TimeField()
    # Ubicación donde se extravió la mascota
    region_extravio = models.ForeignKey(Region, on_delete=models.CASCADE, default="")
    comuna_extravio = models.ForeignKey(Comuna, on_delete=models.CASCADE, default="")
    # Indica si la mascota tiene un chip de identificación
    tiene_chip = models.BooleanField(default=False, blank=True, null=True)
    # Descripción de la mascota
    descripcion = models.TextField()
    # Relación Many-to-Many con el modelo FotosMascota para almacenar fotos de la mascota
    fotos = models.ManyToManyField('FotosMascota', blank=True)
    # Especie de la mascota (puede ser nulo o estar en blanco)
    especie = models.CharField(max_length=100, blank=True, null=True)
    # Color de la mascota, con valor por defecto 'Desconocido'
    color = models.CharField(default='Desconocido', max_length=100)
    # Raza de la mascota (puede ser nulo o estar en blanco)
    raza = models.CharField(max_length=100, blank=True, null=True)
    # Usuario asociado a la mascota
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    def ubicacion_extravio(self):
        return str(self.comuna_extravio) + ", " + str(self.region_extravio)
    # Método para representar la instancia de la clase como una cadena (usado en el admin de Django)
    def __str__(self):
        return self.nombre
    
    
# Modelo para representar una foto de la mascota
class FotosMascota(models.Model):
    # Archivo de imagen de la mascota
    archivo = models.ImageField()

    # Método para representar la instancia de la clase como una cadena (usado en el admin de Django)
    def __str__(self):
        return self.archivo.name
