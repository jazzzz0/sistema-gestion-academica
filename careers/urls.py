from django.urls import path
from . import views

app_name = 'careers'

urlpatterns = [
    # Listado de carreras
    path('', views.CareerListView.as_view(), name='career_list'),

    # Creación
    path('create/', views.CareerCreateView.as_view(), name='career_create'),
    # Detalle
    path('<int:pk>/', views.CareerDetailView.as_view(), name='career_detail'),
    # Actualizar
    path("<int:pk>/update/", views.CareerUpdateView.as_view(), name="career_update"),
    path("<int:pk>/toggle-status/", views.CareerToggleActiveView.as_view(), name="career_toggle_status"),

    # Asignación de materias
    path('<int:pk>/subjects/', views.CareerSubjectsUpdateView.as_view(), name='career_subjects_update'),
]
