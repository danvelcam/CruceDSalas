# authentication/admin.py
from django.contrib import admin
from app.authentication.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("name", "surname", "email", "dni")
    search_fields = ("name", "surname", "email", "dni")
