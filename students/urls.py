from django.urls import path
from . import views

app_name = 'students'

urlpatterns = [
    path('', views.StudentListView.as_view(), name='student_list'),
    path('create/', views.StudentCreateView.as_view(), name='student_create'),
    path('<int:pk>/', views.StudentDetailView.as_view(), name='student_detail'),
    path("<int:pk>/update/", views.StudentUpdateView.as_view(), name="student_update"),
    path("<int:pk>/career/", views.StudentCareerUpdateView.as_view(), name="student_update_career"),
    path('<int:pk>/toggle-active/', views.StudentToggleActiveView.as_view(), name='toggle_student_active'),
]
