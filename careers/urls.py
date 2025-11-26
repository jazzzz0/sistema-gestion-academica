from django.urls import path
from . import views
from .views import CareerUpdateView

app_name = 'careers'

urlpatterns = [
    # Listado (necesario para el botón Cancelar)
    # path('', views.index, name='career_list'),

    # Creación
    path('create/', views.CareerCreateView.as_view(), name='career_create'),
    path("<int:pk>/update/", CareerUpdateView.as_view(), name="career_update"),
]
