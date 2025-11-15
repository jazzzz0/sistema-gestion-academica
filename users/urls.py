from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import DashboardView, ProfileView, HomeView

app_name = "users"  # IMPORTANTE para el namespace

urlpatterns = [
    path(
        "login/",
        LoginView.as_view(
            template_name="registration/login.html",
            redirect_authenticated_user=True
        ),
        name="login"
    ),
    path(
        "logout/",
        LogoutView.as_view(),
        name="logout"
    ),
    path(
        "dashboard/",
        DashboardView.as_view(),
        name="dashboard"
    ),
    path(
        "profile/",
        ProfileView.as_view(),
        name="profile"
    ),
]
