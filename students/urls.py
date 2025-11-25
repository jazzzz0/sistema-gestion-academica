from django.urls import path
from . import views
from .views import StudentDetailView

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:pk>/', StudentDetailView.as_view(), name='student-detail'),
]