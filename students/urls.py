from django.urls import path
from .views import StudentListView, StudentCreateView, StudentUpdateView
app_name = 'students'

urlpatterns = [
    path('', StudentListView.as_view(), name='student_list'),
    path('create/', StudentCreateView.as_view(), name='student_create'),
    path("<int:pk>/edit/", StudentUpdateView.as_view(), name="student_update"),
]