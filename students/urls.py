from django.urls import path
from . import views
from .views import StudentCreateView, StudentUpdateView, StudentListView, StudentCareerUpdateView

app_name = 'students'

urlpatterns = [
    path('', StudentListView.as_view(), name='student_list'),
    path('create/', StudentCreateView.as_view(), name='student_create'),
    path("<int:pk>/edit/", StudentUpdateView.as_view(), name="student_update"),
    path("<int:pk>/career/", StudentCareerUpdateView.as_view(), name="student_update_career"),
]
