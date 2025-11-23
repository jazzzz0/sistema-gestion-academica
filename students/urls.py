from django.urls import path
from . import views
from .views import StudentCreateView, StudentUpdateView
app_name = 'students'

urlpatterns = [
    # path('', views.index, name="student-list"),
    path("create/", StudentCreateView.as_view(), name="student-create"),
    path("<int:pk>/edit/", StudentUpdateView.as_view(), name="student-update"),
    ]
