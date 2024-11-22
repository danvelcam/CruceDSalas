from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
import random
import datetime
from app.utils.crypto import encrypt_cbc, decrypt_cbc, key

class UserManager(BaseUserManager):
    def create_user(self, name, surname, email, dni, tlf, pin, is_admin=False):
        if not dni:
            raise ValueError("Users must have a DNI")
        user = self.model(
            name=name,
            surname=surname,
            email=encrypt_cbc(self.normalize_email(email), key),
            dni=encrypt_cbc(dni,key),
            tlf=encrypt_cbc(tlf,key)
        )
        user.set_password(pin)
        if is_admin:
            user.is_admin = True
            user.is_superuser = True
            user.is_staff = True

        user.save(using=self._db)
        return user

    def create_superuser(self, name, surname, email, dni, tlf, pin):
        user = self.create_user(
            name=name,
            surname=surname,
            email=email,
            dni=dni,
            tlf=tlf,
            pin=pin,
            is_admin=True
        )        
        return user
    

class User(AbstractBaseUser):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, null=False)
    surname = models.CharField(max_length=50, null=False)
    email = models.EmailField(null=True)
    dni = models.CharField(max_length=9, unique=True, null=False)
    tlf = models.CharField(max_length=9, null=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    
    objects = UserManager()

    USERNAME_FIELD = "dni"
    REQUIRED_FIELDS = ["name", "surname", "email", "tlf"]

    def __str__(self):
        return f"{self.name} {self.surname}"

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
    
    def decrypt_value(self, value, plain_text):
        return decrypt_cbc(value, key, plain_text)

    def get_decrypted_dni(self):
        return self.decrypt_value(self.dni, self.dni)

    def get_decrypted_tlf(self):
        return self.decrypt_value(self.tlf, self.tlf)
