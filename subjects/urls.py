from django.urls import path
from . import views

app_name = 'subjects'

urlpatterns = [
    # Listado de materias
    path("", views.SubjectListView.as_view(), name="subject_list"),

    # Individual
    path("<int:pk>/", views.SubjectDetailView.as_view(), name="subject_detail"),

    # Creación
    path("create/", views.SubjectCreateView.as_view(), name="subject_create"),

    # Edición
    path("update/<int:pk>/", views.SubjectUpdateView.as_view(), name="subject_update"),

    # Eliminación
    path("delete/<int:pk>/", views.SubjectDeleteView.as_view(), name="subject_delete"),

    # Materias asignadas a un docente
    path('my-subjects/', views.MySubjectsListView.as_view(), name='my_subjects'),
    path('my-subjects/<int:pk>/students/', views.SubjectEnrollmentListView.as_view(), name='subject_enrollment_list'),
]
