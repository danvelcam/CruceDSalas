# Generated by Django 5.1.3 on 2024-12-05 15:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0004_merge_0002_alter_user_dni_0003_seeders'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='tlf',
            field=models.CharField(max_length=9),
        ),
    ]
