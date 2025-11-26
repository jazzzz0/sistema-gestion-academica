from django.urls import path
from . import views

app_name = 'careers'

urlpatterns = [
    # Listado de carreras
    path('', views.CareerListView.as_view(), name='career_list'),

    # Creación
    path('create/', views.CareerCreateView.as_view(), name='career_create'),

    # Actualización
    path("<int:pk>/update/", views.CareerUpdateView.as_view(), name="career_update"),

    # Asignación de materias
    path('<int:pk>/subjects/', views.CareerSubjectsUpdateView.as_view(), name='career_subjects_update'),

    # Eliminación
    path('<int:pk>/delete/', views.CareerDeleteView.as_view(), name='career_delete'),
]
