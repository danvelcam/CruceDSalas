# autenticacion/models.py
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, name, surname, email, dni):
        if not dni:
            raise ValueError('Users must have a DNI')
        user = self.model(
            name=name,
            surname=surname,
            email=self.normalize_email(email),
            dni=dni,
        )
        user.set_password(dni)  # Set the password to be the DNI
        user.save(using=self._db)
        return user

    def create_superuser(self, name, surname, email, dni):
        user = self.create_user(
            name=name,
            surname=surname,
            email=email,
            dni=dni,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    id = models.AutoField(primary_key=True) 
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    email = models.EmailField(null=True)
    dni = models.CharField(max_length=9, unique=True)

    objects = UserManager()

    USERNAME_FIELD = 'dni'
    REQUIRED_FIELDS = ['name', 'surname', 'email']

    def __str__(self):
        return f"{self.name} {self.surname}"

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin