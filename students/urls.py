from django.urls import path
from . import views

urlpatterns = [
    path('', views.StudentListView.as_view(), name='student_list'),
    path('create/', views.StudentCreateView.as_view(), name='student_create'),
    path("<int:pk>/edit/", views.StudentUpdateView.as_view(), name="student_update"),
    path('<int:pk>/', views.StudentDetailView.as_view(), name='student-detail'),
]