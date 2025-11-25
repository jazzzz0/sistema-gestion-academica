"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from users.views import HomeView, DashboardView, ProfileView


urlpatterns = [
    path('admin/', admin.site.urls),

    # Páginas principales
    path("", HomeView.as_view(), name="home"),  # Página de inicio en /
    path("dashboard/", DashboardView.as_view(), name="dashboard"),  # Dashboard post-login
    path("profile/", ProfileView.as_view(), name="profile"),  # Perfil de usuario

    # Autenticación de Django (login, logout, password_reset, etc.)
    path("", include("django.contrib.auth.urls")),

    # URLs de gestión de profesores
    path("users/", include("users.urls")),

    # URLs de otras apps
    path('students/', include('students.urls')),
    path('careers/', include('careers.urls')),
    path("enrollments/", include("enrollments.urls")),
    path('subjects/', include('subjects.urls')),
]
