from django.urls import path
from users import views

app_name = "users"

urlpatterns = [
    # Vistas generales a todos los usuarios
    path("", views.HomeView.as_view(), name="home"),
    path("dashboard/", views.DashboardView.as_view(), name="dashboard"),
    path("profile/", views.ProfileView.as_view(), name="profile"),

    # Vistas de profesores
    # path("teacher/", TeacherListView.as_view(), name="teacher-list"),
    # path("teacher/create/", TeacherCreateView.as_view(), name="teacher-create"),

]

