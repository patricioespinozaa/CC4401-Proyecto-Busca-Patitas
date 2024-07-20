from django.test import TestCase
from django.urls import reverse
from .models import Mascota, User
from datetime import date, time

class MascotaModelTest(TestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345', email='testuser@example.com')
        self.mascota = Mascota.objects.create(
            usuario=self.user,
            nombre='Firulais',
            fecha_extravio=date(2024, 7, 14),  # Utilisation de date() pour la date
            hora_extravio=time(12, 0),  # Utilisation de time() pour l'heure
            ubicacion_extravio='Parque central',
            tiene_chip=True,
            descripcion='Un perro de tamaño mediano con pelaje marrón.',
            especie='Perro',
            color='Marrón',
            raza='Labrador'
        )

    def test_mascota_creation(self):
        self.assertEqual(self.mascota.nombre, 'Firulais')
        self.assertEqual(self.mascota.fecha_extravio.strftime('%Y-%m-%d'), '2024-07-14')
        self.assertEqual(self.mascota.hora_extravio.strftime('%H:%M:%S'), '12:00:00')
        self.assertEqual(self.mascota.ubicacion_extravio, 'Parque central')
        self.assertTrue(self.mascota.tiene_chip)
        self.assertEqual(self.mascota.descripcion, 'Un perro de tamaño mediano con pelaje marrón.')
        self.assertEqual(self.mascota.especie, 'Perro')
        self.assertEqual(self.mascota.color, 'Marrón')
        self.assertEqual(self.mascota.raza, 'Labrador')
        self.assertEqual(self.mascota.usuario.username, 'testuser')

class MascotaViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345', email='testuser@example.com')
        self.mascota = Mascota.objects.create(
            usuario=self.user,
            nombre='Firulais',
            fecha_extravio=date(2024, 7, 14),  # Utilisation de date() pour la date
            hora_extravio=time(12, 0),  # Utilisation de time() pour l'heure
            ubicacion_extravio='Parque central',
            tiene_chip=True,
            descripcion='Un perro de tamaño mediano con pelaje marrón.',
            especie='Perro',
            color='Marrón',
            raza='Labrador'
        )

    def test_mascota_list_view(self):
        response = self.client.get(reverse('mascota_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Firulais')
        self.assertTemplateUsed(response, 'mascota_list.html')

    def test_mascota_detail_view(self):
        response = self.client.get(reverse('mascota_detail', args=[self.mascota.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Firulais')
        self.assertTemplateUsed(response, 'mascota_detail.html')
