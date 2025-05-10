from django.urls import path
from django.contrib.auth import views as auth_views
from .forms import CustomPasswordResetForm, CustomPasswordResetConfirmForm
from . import views


urlpatterns = [
    path("login", views.user_login, name="login"),
    path("logout", views.custom_logout, name="logout"),
    path("password-change", views.ChangePassword.as_view(), name="password_change"),
    path("reset/<uidb64>/<token>/",
        views.ResetPasswordConfirm.as_view(),
        name="password_reset_confirm",
    ),
    path("register", views.register, name="register"),
    path("update", views.edit, name="edit"),
    path("security", views.security, name="security"),
    path("settings", views.settings, name="settings"),
    path("", views.dashboard, name="dashboard"),
    path("password_reset", views.ResetPasswordForm.as_view(), name="password_reset"),
    path("password_reset/done", views.ResetPasswordDone.as_view(), name="password_reset_done")
]
