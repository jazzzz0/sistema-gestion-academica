from django.urls import path
from . import views

app_name = 'students'

urlpatterns = [
    # path('', views.index, name="student-list"),
    path("create/", views.StudentCreateView.as_view(), name="student-create")
]
