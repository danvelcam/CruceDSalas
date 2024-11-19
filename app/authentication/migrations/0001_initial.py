# Generated by Django 5.1 on 2024-11-16 18:52

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=50)),
                ("surname", models.CharField(max_length=50)),
                ("email", models.EmailField(max_length=254, null=True)),
                ("dni", models.CharField(max_length=9, unique=True)),
                ("tlf", models.CharField(max_length=9)),
            ],
            options={
                "abstract": False,
            },
        ),
    ]