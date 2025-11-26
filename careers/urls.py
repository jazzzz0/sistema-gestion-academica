from django.urls import path
from . import views

app_name = 'careers'

urlpatterns = [
    # Listado (necesario para el botón Cancelar)
    # path('', views.index, name='career_list'),

    # Creación
    path('create/', views.CareerCreateView.as_view(), name='career_create'),

    # Asignación de materias
    path('<int:pk>/subjects/', views.CareerSubjectsUpdateView.as_view(), name='career_subjects_update'),
]
