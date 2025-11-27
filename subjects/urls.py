from django.urls import path
from . import views
from .views import SubjectDetailView

app_name = 'subjects'

urlpatterns = [
    
    # Listado
    # path('', views.index, name="subject_list"),

    # Creación
    path("create/", views.SubjectCreateView.as_view(), name="subject_create"),
    path("<int:pk>/", SubjectDetailView.as_view(), name="subject_detail"),
    
]