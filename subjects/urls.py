from django.urls import path
from . import views

app_name = 'subjects'

urlpatterns = [
    # Listado
    # path('', views.index, name="subject-list"),

    # Creación
    path("create/", views.SubjectCreateView.as_view(), name="subject-create")
]
