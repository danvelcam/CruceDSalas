# auth/urls.py
from django.urls import path
from . import views
from app.home.views import home

urlpatterns = [
    path("register/", views.register, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path('', home,name='home'),

]
