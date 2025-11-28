from django.urls import path

# Solo importamos lo que realmente existe
from users.views.admin_views import AdminListView
from users.views.teacher_views import TeacherCreateView

app_name = "users"

urlpatterns = [
    # Profesores
    path("teachers/create/", TeacherCreateView.as_view(), name="teacher_create"),

    # Administradores
    path("admins/", AdminListView.as_view(), name="admin_list"),

    # Estas rutas NO deben usarse hasta que existan las vistas
    # path("admins/create/", AdminCreateView.as_view(), name="admin_create"),
    # path("admins/<int:pk>/delete/", AdminDeleteView.as_view(), name="admin_delete"),
]
from django.views.generic import TemplateView          