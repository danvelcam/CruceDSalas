from django.db import migrations


def crear_salas_iniciales(apps, schema_editor):
    Sala = apps.get_model("rooms", "Sala")

    salas = [
        {
            "nombre": "Biblioteca",
            "descripcion": "Sala de estudio silenciosa con capacidad para 30 personas. Equipada con mesas individuales, enchufes y wifi.",
            "imagen": "images/biblioteca.jpg",
        },
        {
            "nombre": "Sala de fiestas",
            "descripcion": "Sala para reuniones y eventos. Cuenta con proyector, mesa y sillas para 12 personas.",
            "imagen": "images/sala_de_fiestas.jpg",
        },
        {
            "nombre": "Sala de Informática",
            "descripcion": "Espacio para el uso de material informático con acceso a internet. Ambiente tranquilo y bien iluminado.",
            "imagen": "images/sala_informática_2.jpg",
        },
    ]

    for sala_data in salas:
        Sala.objects.create(**sala_data)


def eliminar_salas(apps, schema_editor):
    Sala = apps.get_model("rooms", "Sala")
    Sala.objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [
        ("rooms", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(crear_salas_iniciales, eliminar_salas),
    ]
