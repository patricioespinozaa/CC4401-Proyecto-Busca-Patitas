# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from todoapp.models import User
from todoapp.models import Mascota
import json

from django.http import HttpResponseRedirect, HttpResponse
from todoapp.models import User  
from todoapp.models import Mascota       
from todoapp.models import FotosMascota
from todoapp.models import Region, Comuna
from django.contrib.auth import authenticate, login,logout
# Mensajes de error
from django.contrib import messages
# Decorador para verificar si el usuario ha iniciado sesión
from django.contrib.auth.decorators import login_required
# Redireccionar a una URL después de que el usuario haya iniciado sesión
from django.urls import reverse
# Importar make_password para encriptar la contraseña
from django.contrib.auth.hashers import make_password
from PIL import Image
# Barra de Busqueda
from django.http import JsonResponse
from django.core.paginator import Paginator
import json
# Diccionario de especies y razas
especie_raza = {
    'Perro': ['Labrador Retriever', 'Golden Retriever', 'Pastor Alemán', 'Bulldog Francés', 'Bulldog Inglés', 'Chihuahua', 'Boxer', 'Dálmata', 'Poodle', 'Pug', 'Quiltro'],
    'Gato': ['Siamés', 'Persa', 'Maine Coon', 'Bengalí', 'Ragdoll', 'British Shorthair', 'Sphynx', 'Abisinio', 'Birmano', 'American Shorthair', 'Gato mestizo'],
    'Ave': ['Canario', 'Periquito', 'Cacatúa', 'Cotorra', 'Periquito Australiano', 'Diamante Mandarín', 'Agapornis', 'Calafate'],
    'Reptil': ['Gecko leopardo', 'Iguana verde', 'Tortuga de orejas rojas', 'Dragón barbudo', 'Tortuga rusa', 'Python real', 'Boa constrictor', 'Gecko crestado', 'Tortuga mediterránea', 'Tortuga de tierra'],
    'Roedor': ['Cobaya', 'Hámster', 'Rata doméstica', 'Conejo', 'Chinche degú', 'Jerbo', 'Cuyo', 'Ratón doméstico', 'Criceto', 'Cuyo de pelo largo']
}

def busqueda(request):
    query = request.GET.get('q', '')
    especie = request.GET.get('especie', '')
    color = request.GET.get('color', '')
    raza = request.GET.get('raza', '')
    tiene_chip = request.GET.get('tiene_chip', '')
    region = request.GET.get('region', '')
    comuna = request.GET.get('comuna', '')

    mascotas = Mascota.objects.all()

    # Aplicar filtros según los parámetros de búsqueda
    if query:
        mascotas = mascotas.filter(nombre__icontains=query)
    if especie: 
        mascotas = mascotas.filter(especie=especie)
    if color:
        mascotas = mascotas.filter(color=color)
    if raza:
        mascotas = mascotas.filter(raza=raza)
    if region:
        try:
            region = Region.objects.get(region = region)
            idregion = region.id
            mascotas = mascotas.filter(region_extravio=idregion)
        except Region.DoesNotExist:
            print("Tabla region no existe")
    if comuna:
        try:
            comuna = Comuna.objects.get(comuna = comuna)
            idcomuna = comuna.id
            mascotas = mascotas.filter(comuna_extravio=idcomuna)
        except Comuna.DoesNotExist:
            print("Tabla comuna no existe")
    if tiene_chip:
        mascotas = mascotas.filter(tiene_chip=(tiene_chip.lower() == 'true'))

    mascotas = mascotas.order_by('nombre');
    paginator = Paginator(mascotas, 10)  # Mostrar 6 mascotas por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        results = []
        for mascota in page_obj:
            results.append({
                'id': mascota.id,
                'nombre': mascota.nombre,
                'fecha_extravio': mascota.fecha_extravio.strftime('%d/%m'),
                'ubicacion_extravio': mascota.ubicacion_extravio,
                'raza': mascota.raza,
                'color': mascota.color,
                'descripcion': mascota.descripcion,
                'foto_url': mascota.fotos.first().archivo.url if mascota.fotos.exists() else None
            })
        return JsonResponse({'mascotas': results, 'has_next': page_obj.has_next()})
    else:
        return render(request, 'todoapp/home.html', {'mascotas': page_obj, 'especie_raza': especie_raza})

def filtrar_mascotas(request):
    if request.method == 'GET':
        # Atributos a filtrar
        #fubicacion = request.GET.get('fubicacion')
        ftiene_chip = request.GET.get('fchip')
        fespecie = request.GET.get('fespecie')
        fcolor = request.GET.get('fcolor')
        fraza = request.GET.get('fraza')

        #Falta implementar diccionario antes de usar estos atributos
        fregion = request.GET.get('fregion')
        fcomuna = request.GET.get('fcomuna')

        campos = {'tiene_chip': ftiene_chip, 'especie': fespecie, 'color': fcolor, 'raza': fraza}
        filtros = campos_filtrados(campos)

        # Filtrar mascotas por sus atributos
        mascotas_filtrados = Mascota.objects.filter(**filtros)

        paginator = Paginator(mascotas_filtrados, 6)  # Mostrar 6 mascotas por página
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            results = []
            for mascotas_filtrados in page_obj:
                results.append({
                    'id': mascotas_filtrados.id,
                    'nombre': mascotas_filtrados.nombre,
                    'fecha_extravio': mascotas_filtrados.fecha_extravio.strftime('%d/%m'),
                    'ubicacion_extravio': mascotas_filtrados.ubicacion_extravio,
                    'color': mascotas_filtrados.color,
                    'descripcion': mascotas_filtrados.descripcion,
                    'foto_url': mascotas_filtrados.fotos.first().archivo.url if mascotas_filtrados.fotos.exists() else None
                })
            return JsonResponse({'mascotas': results, 'has_next': page_obj.has_next()})
        
        # Pasar los productos filtrados al template
        return render(request, 'todoapp/home.html', {'mascotas': page_obj})

def campos_filtrados(list):
    result = list.copy()
    for atrib, valor in result.items():
        if valor is None or valor == '':
            list.pop(atrib)
    return list

# Registro de Usuario
def register_user(request):
    # Método GET
    if request.method == 'GET':                                     
        return render(request, "todoapp/register_user.html")            # Muestra la página de registro
    # Método POST
    elif request.method == 'POST':
        nombre = request.POST['nombre']                                 # Obtener el nombre del formulario
        mail = request.POST['mail']                                     # Obtener el correo electrónico del formulario
        contraseña = request.POST['contraseña']                         # Obtener la contraseña del formulario
        confirm_contraseña = request.POST['confirm_contraseña']         # Obtener la confirmación de la contraseña del formulario

        #Obtenemos los datos de los usuarios de la base de datos
        namesAndmails = User.objects.values_list('username', 'email')

        # Verificar que ambas contraseñas coincidan
        if contraseña != confirm_contraseña:
            messages.error(request, 'Las contraseñas no coinciden.') 
            return redirect('register_user')

        #Verificar que nombre y mail no esten registrados previamente
        for nameEmail in namesAndmails:
            name_register, mail_register = nameEmail
            if nombre == name_register:
                messages.error(request, 'Nombre ya registrado, intente con uno distinto.')
                return redirect('register_user')

            if mail == mail_register:
                messages.error(request, 'Correo ya registrado, intente con uno distinto.')
                return redirect('register_user')

        # Crear un nuevo usuario
        user = User.objects.create_user(username=nombre, password=contraseña, email=mail)
        
        # Autenticar al usuario recién registrado
        usuario_autenticado = authenticate(request, username=nombre, password=contraseña)
        if usuario_autenticado:                                         # Redirigir al perfil del usuario si la autenticación es exitosa
            login(request, usuario_autenticado)
            return redirect('perfil_usuario')
        else:                                                           # Mostrar mensaje de error si la autenticación falla
            messages.error(request, 'Ha ocurrido un error al registrar el usuario.')
            return render(request, "todoapp/register_user.html")
        
# Inicio de Sesión:
def login_user(request):
    # Método GET
    if request.method == 'GET':
        if request.user.is_authenticated:                   # Verifica si el usuario ya ha iniciado sesión
            return redirect(reverse('perfil_usuario'))      # Si lo esta, redirige a la página de perfil
        else:
            return render(request, "todoapp/login.html")    # Si no lo esta, muestra la página de inicio de sesión
    # Método Post
    elif request.method == 'POST':
        correo_electronico = request.POST['email']          # Obtener el correo electrónico del formulario
        contraseña = request.POST['contraseña']             # Obtener la contraseña del formulario
        # Obtener el username del usuario a partir del correo electrónico
        username = User.objects.get(email=correo_electronico).username
        # Autenticar al usuario
        usuario = authenticate(username=username,password=contraseña)
        if usuario is not None:                             # Si el usuario existe
            login(request, usuario)
            return HttpResponseRedirect('/perfil_usuario')  # Redirige al perfil del usuario después del inicio de sesión exitoso
        else:
            messages.error(request, 'Correo electrónico o contraseña incorrectos.') # Mensaje de error y redirige a la página de inicio de sesión
            return render(request, "todoapp/login.html")

# Cerrar Sesión
# Requiere que el usuario haya iniciado sesión
@login_required
def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/inicio')               # Warning: Deberia redirigir a la página de inicio (no existe aún)

# Perfil de Usuario
# Requiere que el usuario haya iniciado sesión
@login_required
def perfil_usuario(request):
    user = request.user

    publicaciones = Mascota.objects.filter(usuario=user)
    
    # Guardar los cambios realizados en el perfil
    if request.method == 'POST':
        if 'guardar_celular' in request.POST:                                   
            user.celular = request.POST.get('celular')
            user.save()
            messages.success(request, 'Celular actualizado correctamente.')
        if 'guardar_ubicacion_personal' in request.POST:
            user.ubicacion_personal = request.POST.get('ubicacion')
            user.save()
            messages.success(request, 'Ubicación personal actualizada correctamente.')
        elif 'guardar_perfil' in request.POST:
            new_username = request.POST.get('nombre')
            if new_username:
                user.username = new_username
            user.ubicacion_personal = request.POST.get('ubicacion')
            user.save()
            messages.success(request, 'Perfil actualizado correctamente.')
        return redirect('perfil_usuario')
    # Mostrar el perfil del usuario
    return render(request, "todoapp/perfil_usuario.html", {'user': user, 'publicaciones': publicaciones})

# Modificar Perfil
# Requiere que el usuario haya iniciado sesión
@login_required
def modificar_perfil(request):
    user = request.user
    if request.method == 'POST':
        # Mantener el mismo username si no se modifica
        new_username = request.POST.get('nombre')
        if new_username:
            user.username = new_username
        user.celular = request.POST.get('celular')
        user.ubicacion_personal = request.POST.get('ubicacion_personal')
        user.save()
        return redirect('perfil_usuario')
    return render(request, "todoapp/modificar_perfil.html", {'user': user})

# Función para verificar si el archivo es una imagen válida (JPEG o PNG)    
def verify_image(f):
    # Verifica el tipo de contenido del archivo    
    if f.content_type not in ['image/jpeg', 'image/png']:
        return False
    try:
        # Intenta abrir y verificar la imagen usando PIL
        with Image.open(f) as img:
            img.verify()
    except IOError:
        # Si hay un error al abrir/verificar la imagen, retorna False
        return False
    # Si la imagen es válida, retorna True    
    return True

# Vista para manejar la creación de una ficha de mascota
def fichaAnimal(request):
    if request.method == 'POST':
        # Obtiene los datos del formulario
        nombre = request.POST.get('nombreAnimal')
        fecha_extravio = request.POST.get('fechaExtravio')
        hora_extravio = request.POST.get('horaExtravio')
        region = request.POST.get('RegionExtravio')
        comuna = request.POST.get('ComunaExtravio')
        especie = request.POST.get('especie')
        color = request.POST.get('color')
        raza = request.POST.get('raza')
        tiene_chip = request.POST.get('tieneChip')
        descripcion = request.POST.get('descripcion')
        fotos = request.FILES.getlist('fotos')
        usuario = request.user

        # Verifica que todos los campos estén llenos
        if all([nombre, fecha_extravio, hora_extravio, region, comuna, especie, color, raza, tiene_chip, descripcion]):
            # Verifica cada foto            
            for foto in fotos:
                if not verify_image(foto):
                    return HttpResponse("Uno o más archivos no están en formato JPEG o PNG o están corruptos.", status=400)

            reg = Region.objects.get(region = region)

            comu = Comuna.objects.get(region = reg, comuna = comuna)
            
            # Crea una nueva instancia de Mascota y la guarda en la base de datos
            nueva_mascota = Mascota(
                nombre=nombre,
                fecha_extravio=fecha_extravio,
                hora_extravio=hora_extravio,
                region_extravio = reg,
                comuna_extravio = comu,
                especie=especie,
                color=color,
                raza=raza,
                tiene_chip=(tiene_chip == 'si'),
                descripcion=descripcion,
                usuario=usuario
            )
            nueva_mascota.save()
            
            # Guarda cada foto asociada a la mascota
            for foto in fotos:
                nueva_foto = FotosMascota.objects.create(archivo=foto)
                nueva_mascota.fotos.add(nueva_foto)

            # Renderiza una página de confirmación
            return render(request, "todoapp/ficha_enviada.html")
        
        else:
            # Retorna un mensaje de error si faltan campos
            print("cosoa")
            print([nombre, fecha_extravio, hora_extravio, region, comuna, especie, color, raza, tiene_chip, descripcion])
            return HttpResponse("Todos los campos son obligatorios")

    else:
        # Renderiza el formulario de ficha de mascota
        return render(request, "todoapp/ficha_animal.html")
    
# Vista para mostrar una imagen específica
def mostrar_imagen(request, foto_id):
    # Obtiene la foto correspondiente al ID, o retorna 404 si no se encuentra
    foto = get_object_or_404(FotosMascota, pk=foto_id)
    # Renderiza la plantilla para mostrar la imagen
    return render(request, 'todoapp/mostrar_imagen.html', {'foto': foto}) 

# Vista de prueba para renderizar un formulario de inicio de sesión
def test_html(request):
    if request.method == 'GET':
        # Renderiza la plantilla de prueba de diseño
        return render(request, "todoapp/design_test.html")
    elif request.method == 'POST':
        # Obtiene los datos del formulario de inicio de sesión
        username = request.POST['username']
        contraseña = request.POST['contraseña']
        # Autentica al usuario
        usuario = authenticate(username=username, password=contraseña)
        if usuario is not None:
            # Inicia sesión si la autenticación es exitosa
            login(request, usuario)
            return HttpResponseRedirect('/tareas')
        else:
            # Redirige a la página de registro si la autenticación falla
            return HttpResponseRedirect('/register') 

# Vista para ver una publicación específica de una mascota
def view_post(request,post_id):
    if request.method == 'GET':
        # try
            # Intenta obtener la mascota con el ID proporcionado
            Mascota.objects.all().get(id = post_id)
            mascota = Mascota.objects.get(id = post_id)
            # Prepara los datos de la publicación para renderizar    
            imageList = []
            for imagen in mascota.fotos.all():
                imageList.append((imagen.archivo.url))
            post_data = {
                "nombre":  mascota.nombre,
                "fecha_extravio": mascota.fecha_extravio,
                "hora_extravio": mascota.hora_extravio,
                "ubicacion_extravio": mascota.ubicacion_extravio,
                "tiene_chip": "si" if mascota.tiene_chip else "no",
                "descripcion": mascota.descripcion,
                "foto1": imageList[0],
                "color": mascota.color,
                "especie": mascota.especie,
                "raza": mascota.raza,
                "fotos": imageList
            }
            # Renderiza la plantilla con los datos de la publicación
            return render(request,"todoapp/view_post.html",post_data)        
        # except:
            # Imprime un mensaje de error si ocurre una excepción
            # print("ERROR al obtener mascota")
            # return HttpResponseRedirect("/inicio")

# Vista para cargar una publicación específica de una mascota
def cargar_post(request,post_id):
    # Obtiene la mascota con el ID proporcionado
    Mascota.objects.all().get(id = post_id)
    mascota = Mascota.objects.get(id = post_id)
    # Prepara los datos de la publicación para renderizar
    imageList = []

    for imagen in mascota.fotos.all():
        imageList.append(imagen.archivo.url)
    if(len(imageList) == 0): #esto en teoria no puede pasar, pero por si acaso
        imageList.append("static/todoapp/img/placeholder.png")    
    post_data = {
        "nombre":  mascota.nombre,
        "fecha_extravio": mascota.fecha_extravio,
        "hora_extravio": mascota.hora_extravio,
        "ubicacion_extravio": mascota.ubicacion_extravio,
        "tiene_chip": "si" if mascota.tiene_chip else "no",
        "descripcion": mascota.descripcion,
        "foto1": imageList[0],
        "color": mascota.color,
        "especie": mascota.especie,
        "raza": mascota.raza,
        "fotos": imageList
    }
    # Renderiza la plantilla con los datos de la publicación
    return render(request,"todoapp/view_post.html",post_data)    
  
# Vista para mostrar el menú principal sin paginación (intermediaria)
def menu_solo(request):
    if request.method == 'GET':
        return menu_principal(request,1)

# Vista principal para mostrar el menú con paginación
def menu_principal(request,page_num):
    if page_num == 0:
        return menu_solo(request)
    if request.method == 'GET':
        
        cells = {}
        range_start = 3*(page_num-1)
        range_end = 3*(page_num)
        posts = Mascota.objects.all()[range_start:range_end]
        
        tam = posts.count()
        i = 1
        #print(posts)
        #print(tam)
        while i < tam+1: #max 3 post por pagina
            
            ind = (str)(i)

            # cells[ind] = posts
            nom = "nombre" + ind
            fecha = "fecha_extravio"+ind
            hora = "hora_extravio"+ind
            ubicacion = "ubicacion_extravio"+ind
            chip = "tiene_chip"+ind
            desc = "descripcion"+ind
            id = "id"+ind

            anim = posts[i-1]

            id_mascota = (str)(anim.id)
            url_post_animal = "url_post"+ind

            id_mascota = (str)(anim.id)
            url_post_animal = "url_post"+ind

            # Guarda los datos de la mascota en el diccionario cells
            cells[nom] = anim.nombre
            cells[fecha] = anim.fecha_extravio
            cells[hora] = anim.hora_extravio
            cells[ubicacion] = anim.ubicacion_extravio
            cells[chip] = "si" if anim.tiene_chip else "no"
            cells[desc] = anim.descripcion
            cells[id] = anim.id
            cells[url_post_animal] = "post/"+id_mascota

            i = i+1
        # Renderiza la plantilla adecuada según la cantidad de publicaciones
        if tam == 3:
            return render(request,"todoapp/Inicio/main_menu3.html",cells)
        elif tam == 2:
            return render(request,"todoapp/Inicio/main_menu2.html",cells)
        elif tam == 1:
            return render(request,"todoapp/Inicio/main_menu1.html",cells)
        elif tam == 0:
            return render(request,"todoapp/Inicio/main_menu0.html",cells)
        else: #usado como error
            return render(request,"todoapp/tareas")
    
    if request.method == 'POST':
        context = {}
        context["page"] = page_num
        if "animal1" in request.POST:
            id = request.POST['animal1']
            #path = "/post/"+id
            #return HttpResponseRedirect(path)
            return cargar_post(request,id)
        elif "animal2" in request.POST:
            id = request.POST['animal2']
            #path = "/post/"+id
            #return HttpResponseRedirect(path)
            return cargar_post(request,id)
        elif "animal3" in request.POST:
            id = request.POST['animal3']
            #path = "/post/"+id
            #return HttpResponseRedirect(path)
            return cargar_post(request,id)


def regiones_comunas(request):
    #procesador de contexto para regiones

    regiones = []
    comunas = {}
    for region in Region.objects.all():
        regiones.append(str(region))
        comunas[str(region)] = []
        for comuna in Comuna.objects.all().filter(region = (region)):
            comunas[str(region)].append(str(comuna))
    return {'REGIONES': regiones, 'COMUNAS': json.dumps(comunas)}
