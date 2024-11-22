# auth/urls.py
from django.urls import path
from . import views
from app.home.views import home
from app.authentication.views import (
    send_verification_code,
    verify_code,
    password_reset_confirm,
)
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("register/", views.register, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("", home, name="home"),
    path(
        "send_verification_code/", send_verification_code, name="send_verification_code"
    ),
    path("verify_code/", verify_code, name="verify_code"),
    path(
        "password_reset/done/",
        auth_views.PasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/", password_reset_confirm, name="password_reset_confirm"
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
]
