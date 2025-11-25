from django.urls import path
# from users.views import TeacherListView, TeacherCreateView

app_name = "users"

urlpatterns = [
    # Vistas de gestión de profesores (descomentarlas cuando estén implementadas)
    # path("teachers/", TeacherListView.as_view(), name="teacher-list"),
    # path("teachers/create/", TeacherCreateView.as_view(), name="teacher-create"),
    # path("teachers/<int:pk>/edit/", TeacherUpdateView.as_view(), name="teacher-update"),
    # path("teachers/<int:pk>/delete/", TeacherDeleteView.as_view(), name="teacher-delete"),
]
