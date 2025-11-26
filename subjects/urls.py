from django.urls import path
from . import views
from .views import SubjectListView

app_name = 'subjects'

urlpatterns = [
    # Listado
    # path('', views.index, name="subject_list"),

    # Creación
    path("create/", views.SubjectCreateView.as_view(), name="subject_create"),  # <-- comma added

    # Listado de materias
    path("", SubjectListView.as_view(), name="subject_list"),
]
