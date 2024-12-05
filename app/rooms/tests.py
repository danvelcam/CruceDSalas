from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from app.rooms.models import Sala, Reserva, Valoracion
from app.authentication.models import User
from datetime import timedelta


class RoomsTests(TestCase):
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

        # Crear una sala de prueba
        self.sala = Sala.objects.create(
            nombre="Sala de reuniones",
            descripcion="Sala equipada con proyector y 10 sillas.",
        )

        # Inicia sesión como el usuario creado
        self.client.login(username=self.dni, password=self.pin)

    def test_lista_salas(self):
        """Prueba la lista de salas."""
        response = self.client.get(reverse("lista_salas"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Sala de reuniones")  # Verifica la sala en la lista

    def test_reserva_sala_get(self):
        """Prueba el acceso al formulario de reserva de sala."""
        response = self.client.get(reverse("reserva_sala", args=[self.sala.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Reservar Sala de reuniones")  # Verifica el formulario

    def test_reserva_sala_post(self):
        """Prueba la creación de una reserva."""
        fecha = timezone.now().date()
        response = self.client.post(reverse("reserva_sala", args=[self.sala.id]), {
            "fecha": fecha,
            "hora_inicio": "10:00",
            "hora_fin": "11:00",
            "asunto": "Reunión semanal",
        })
        self.assertEqual(response.status_code, 302)  # Redirige tras la reserva
        self.assertTrue(Reserva.objects.filter(usuario=self.user, sala=self.sala).exists())

    def test_valorar_experiencia(self):
        """Prueba valorar una experiencia."""
        response = self.client.post(reverse("valorar_experiencia"), {"valoracion": "positiva"})
        self.assertEqual(response.status_code, 302)  # Redirige tras valorar
        self.assertTrue(Valoracion.objects.filter(satisfecho=True).exists())

    def test_mis_reservas(self):
        """Prueba la vista de reservas del usuario."""
        Reserva.objects.create(
            sala=self.sala,
            usuario=self.user,
            fecha=timezone.now().date(),
            hora_inicio="10:00",
            hora_fin="11:00",
            asunto="Reunión semanal",
        )
        response = self.client.get(reverse("mis_reservas"))
        self.assertEqual(response.status_code, 200)
        # Verificar que el asunto, la sala y el estado estén presentes en la respuesta
        self.assertContains(response, "Sala de reuniones")
        self.assertContains(response, "10:00")
        self.assertContains(response, "11:00")
        self.assertContains(response, "PENDIENTE")  # Estado inicial

    def test_cancelar_reserva(self):
        """Prueba cancelar una reserva."""
        reserva = Reserva.objects.create(
            sala=self.sala,
            usuario=self.user,
            fecha=timezone.now().date(),
            hora_inicio="10:00",
            hora_fin="11:00",
            asunto="Reunión semanal",
        )
        response = self.client.post(reverse("cancelar_reserva", args=[reserva.id]))
        self.assertEqual(response.status_code, 302)  # Redirige tras cancelar
        self.assertFalse(Reserva.objects.filter(id=reserva.id).exists())
