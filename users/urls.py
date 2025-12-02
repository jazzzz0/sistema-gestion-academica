from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    # Vistas de gestión de profesores
    path("teachers/", views.TeacherListView.as_view(), name="teacher_list"),
    path("teachers/create/", views.TeacherCreateView.as_view(), name="teacher_create"),
    path("teachers/<int:pk>/delete/", views.TeacherDeleteView.as_view(), name="teacher_delete"),

    # Vistas de gestión de administradores
    path("admins/", views.AdminListView.as_view(), name="admin_list"),
    path("admins/create/", views.AdminCreateView.as_view(), name="admin_create"),
    path("admins/<int:pk>/delete/", views.AdminDeleteView.as_view(), name="admin_delete"),

    # Vistas de auth
    path("first-login-change-password/", views.FirstLoginChangePasswordView.as_view(), name="first_login_change_password"),
    path('password-change/', views.UserPasswordChangeView.as_view(), name='password_change'),
]
