from django.urls import path
from . import views

app_name = 'careers'

urlpatterns = [
    # Listado de carreras
    path('', views.CareerListView.as_view(), name='career_list'),

    # Creación
    path('create/', views.CareerCreateView.as_view(), name='career_create'),
]
