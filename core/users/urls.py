from django.urls import path
from django.contrib.auth import views as auth_views
from .views import signup_view, login_view, logout_view, settings_view

urlpatterns = [
    # User auth and sessions management
    path("signup/", signup_view, name="signup"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("settings/", settings_view, name="settings"),
    # Password resets
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name="auth/password_reset.html"), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name="auth/password_reset_done.html"), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="auth/password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name="auth/password_reset_complete.html"), name='password_reset_complete'),
]
