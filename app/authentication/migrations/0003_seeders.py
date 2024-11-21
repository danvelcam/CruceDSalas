from django.db import migrations
from app.authentication.models import User

def create_users(apps, schema_editor):
    User.objects.create_superuser(
        name='admin',
        surname='admin',
        email='admin_email@example.com',
        dni='12345678Z',
        tlf='987654321',
        pin='1234'
    )

    User.objects.create_user(
        name='Daniel',
        surname='Vela',
        email='user_email@example.com',
        pin='1234',
        dni='49786191T',
        tlf='123456789'
        )

class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_user_is_active_user_is_admin_user_is_superuser'),
    ]

    operations = [
        migrations.RunPython(create_users),
    ]