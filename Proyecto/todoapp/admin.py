from django.contrib import admin

# Register your models here.
from todoapp.models import User, Categoria , Mascota, FotosMascota
from categorias.models import Categoria
 
admin.site.register(Categoria)
admin.site.register(User)
#admin.site.register(Tarea)
#admin.site.register(Mascota)
#admin.site.register(FotosMascota)

