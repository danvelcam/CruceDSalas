from django.test import TestCase
from django.urls import reverse
from app.authentication.models import User, encrypt_cbc, decrypt_cbc, key


class UserTests(TestCase):
    def setUp(self):
        """
        Configuración inicial para los tests:
        - Crea un usuario con datos encriptados.
        """
        self.dni = "12345678A"
        self.pin = "1234"
        self.name = "Test"
        self.surname = "User"
        self.email = "test@example.com"
        self.tlf = "600123456"

        # Crear un usuario con datos encriptados
        self.user = User.objects.create_user(
            name=self.name,
            surname=self.surname,
            email=self.email,
            dni=self.dni,
            tlf=self.tlf,
            pin=self.pin,
        )

    def test_user_creation(self):
        """Prueba la creación de usuarios y la encriptación de datos sensibles."""
        self.assertTrue(isinstance(self.user, User))
        self.assertEqual(self.user.name, self.name)
        self.assertEqual(self.user.surname, self.surname)
        self.assertEqual(decrypt_cbc(self.user.email, key, self.email), self.email)
        self.assertEqual(decrypt_cbc(self.user.dni, key, self.dni), self.dni)
        self.assertEqual(decrypt_cbc(self.user.tlf, key, self.tlf), self.tlf)
        self.assertTrue(self.user.check_password(self.pin))

    def test_superuser_creation(self):
        """Prueba la creación de superusuarios."""
        admin = User.objects.create_superuser(
            name="Admin",
            surname="User",
            email="admin@example.com",
            dni="87654321B",
            tlf="700123456",
            pin="admin123",
        )
        self.assertTrue(admin.is_superuser)
        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.is_admin)

    def test_user_login_valid(self):
        """Prueba el inicio de sesión con credenciales válidas."""
        response = self.client.post(reverse("login"), {"dni": self.dni, "pin": self.pin})
        self.assertEqual(response.status_code, 302)  # Redirige después del login
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_user_login_invalid(self):
        """Prueba el inicio de sesión con credenciales inválidas."""
        response = self.client.post(reverse("login"), {"dni": "wrongdni", "pin": "wrongpin"})
        self.assertEqual(response.status_code, 200)  # Se queda en la página de login
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_logout(self):
        """Prueba el cierre de sesión."""
        self.client.login(username=self.dni, password=self.pin)
        response = self.client.post(reverse("logout"))
        self.assertEqual(response.status_code, 302)  # Redirige a 'home'
        self.assertFalse(response.wsgi_request.user.is_authenticated)

