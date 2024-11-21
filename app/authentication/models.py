from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
import random
import datetime
from dotenv import load_dotenv
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Hash import HMAC, SHA256
import base64
import os

load_dotenv()

key_base64 = os.getenv("AES_KEY")
key = base64.b64decode(key_base64)


def derive_iv(data, key):
    h = HMAC.new(key, digestmod=SHA256)
    h.update(data.encode())
    return h.digest()[:16] 

def encrypt_cbc(plain_text, key):
    iv = derive_iv(plain_text, key)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded_text = pad(plain_text.encode(), AES.block_size)
    encrypted_text = cipher.encrypt(padded_text)
    return base64.b64encode(encrypted_text).decode()

def decrypt_cbc(encrypted_text, key, plain_text):
    iv = derive_iv(plain_text, key)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decoded_encrypted_text = base64.b64decode(encrypted_text)
    decrypted_text = unpad(cipher.decrypt(decoded_encrypted_text), AES.block_size)
    return decrypted_text.decode()


class UserManager(BaseUserManager):
    def create_user(self, name, surname, email, dni, tlf, pin):
        if not dni:
            raise ValueError("Users must have a DNI")
        user = self.model(
            name=name,
            surname=surname,
            email=self.normalize_email(email),
            dni=encrypt_cbc(dni,key),
            tlf=encrypt_cbc(tlf,key)
        )
        user.set_password(pin)
        user.save(using=self._db)
        return user

    def create_superuser(self, name, surname, email, dni, tlf, pin):
        user = self.create_user(
            name=name,
            surname=surname,
            email=email,
            dni=dni,
            tlf=tlf,
            pin=pin
        )
        user.is_admin = True
        user.is_superuser = True
        return user
    
    def generate_random_pin(self):
        return str(random.randint(1000, 9999))
    
    def sms_pin_generator(self, pin, tlf):
        file_path = "sms.log"
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        message = f"Your PIN is {pin}"
        log_entry = f"[{timestamp}] To: {tlf} | Message: \"{message}\" \n"
        with open(file_path, "a") as file:
            file.write(log_entry)


class User(AbstractBaseUser):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, null=False)
    surname = models.CharField(max_length=50, null= False)
    email = models.EmailField(null=True)
    dni = models.CharField(max_length=9, unique=True, null=False)
    tlf = models.CharField(max_length=9, null=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    
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


    @property
    def is_staff(self):
        return self.is_admin
