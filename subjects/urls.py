from django.urls import path
from . import views
from .views import SubjectCreateView, SubjectListView

app_name = 'subjects'

urlpatterns = [
    # Listado de materias
     path("", SubjectListView.as_view(), name="subject_list"),

    # Creación
    path("create/", SubjectCreateView.as_view(), name="subject_create")
]
