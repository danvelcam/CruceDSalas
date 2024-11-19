from django.test import TestCase
from django.urls import reverse
from app.authentication.forms import UserLoginForm
from django.contrib.auth.models import User

class LoginTestCase(TestCase):
    
    def setUp(self):
        # Crear un usuario para las pruebas
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword',
            first_name='Test',
            last_name='User'
        )
    
    def test_login_form_valid(self):
        # Probar el formulario con datos válidos
        form_data = {'name': 'Test', 'surname': 'User', 'dni': '12345678A'}
        form = UserLoginForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_login_form_invalid_dni(self):
        # Probar el formulario con un DNI inválido
        form_data = {'name': 'Test', 'surname': 'User', 'dni': 'INVALID_DNI'}
        form = UserLoginForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_login_view(self):
        # Probar la vista de inicio de sesión con credenciales correctas
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'testpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Inicio de sesión exitoso')

    def test_login_view_invalid(self):
        # Probar la vista de inicio de sesión con credenciales incorrectas
        response = self.client.post(reverse('login'), {
            'username': 'wronguser',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Credenciales inválidas')
