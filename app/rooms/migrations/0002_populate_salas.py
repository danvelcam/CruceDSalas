from django.db import migrations

def crear_salas_iniciales(apps, schema_editor):
    Sala = apps.get_model('rooms', 'Sala')
    
    salas = [
        {
            'nombre': 'Asociación de Mayores y Pensionistas "La Candela"',
            'descripcion': 'Espacio dedicado al bienestar, la integración y la participación de las personas mayores de la localidad.',
            'imagen': 'images/la_candela.png'
        },
        {
            'nombre': 'Asociación Cultural Juvenil "El Patio',
            'descripcion': 'Asociación cultural juvenil que promueve la participación y la integración de los jóvenes en la localidad.',
            'imagen': 'images/el_patio.png'  
        },
        {
            'nombre': 'Salón de la Hermandad de San Sebastián',
            'descripcion': 'Espacio emblemático que sirve como punto de para actividades sociales, culturales y religiosas de la comunidad.',
            'imagen': 'images/san_sebastian.jpg'  
        },
        {
            'nombre': 'Biblioteca Municipal',
            'descripcion': 'Equipado con una amplia colección de libros y recursos multimedia, es un espacio de encuentro y aprendizaje para todos los vecinos.',
            'imagen' : 'images/biblioteca.jpg'
        },
        {
            'nombre': 'Sala Guadalinfo',
            'descripcion': 'Sala equipada con ordenadores y conexión a Internet para fomentar la alfabetización digital y el acceso a la información.',
            'imagen': 'images/sala_informática_2.jpg'
        }
    ]
    
    for sala_data in salas:
        Sala.objects.create(**sala_data)

def eliminar_salas(apps, schema_editor):
    Sala = apps.get_model('rooms', 'Sala')
    Sala.objects.all().delete()

class Migration(migrations.Migration):
    dependencies = [
        ('rooms', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(crear_salas_iniciales, eliminar_salas),
    ]