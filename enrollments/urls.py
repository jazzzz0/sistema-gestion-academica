from django.urls import path
from . import views
from .views import MyEnrollmentListView, EnrollmentDropView

app_name = "enrollments"

urlpatterns = [
    path("", views.inicio, name="inicio"),
    path("my-enrollments/", MyEnrollmentListView.as_view(), name="my_enrollments"),
    path("unenroll/<int:pk>/", EnrollmentDropView.as_view(), name="enrollment_drop"),
]
