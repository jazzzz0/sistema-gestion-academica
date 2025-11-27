from django.urls import path
from . import views

app_name = 'subjects'

urlpatterns = [
    # Listado
    # path("", views.SubjectListView.as_view(), name="subject_list"),

    # Individual
    path("<int:pk>/", views.SubjectDetailView.as_view(), name="subject_detail"),

    # Creación
    path("create/", views.SubjectCreateView.as_view(), name="subject_create"),

    # Edición
    path("update/<int:pk>/", views.SubjectUpdateView.as_view(), name="subject_update"),
]
