from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.busqueda, name='home'),                                                          # URL Interfaz principal
    path('', views.filtrar_mascotas, name='post_filter'),
    path('register', views.register_user, name='register_user'),                                    # URL para registrar usuario
    path('login', views.login_user, name='login'),                                                  # URL para iniciar sesión                             
    path('logout', views.logout_user, name='logout'),                                               # URL para cerrar sesión
    path('perfil_usuario', views.perfil_usuario, name='perfil_usuario'),                            # URL para ver perfil de usuario
    path('design_test',views.test_html, name='design_test'),                                        # URL para probar diseño
    path('post/<int:post_id>',views.view_post,name = 'ver_post'),
    path('inicio/post/<int:post_id>', views.view_post, name = "ver_post_inicio"),
    path('inicio',views.menu_solo,name ='Inicio'),
    path('inicio/<int:page_num>',views.menu_principal,name='Inicio'),
    path('fichaAnimal/', views.fichaAnimal, name= 'ficha_animal'),
    path('mostrar_imagen/<int:foto_id>/', views.mostrar_imagen, name='mostrar_imagen')
] 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)