from django.urls import path
from . import views

app_name = "enrollments"

urlpatterns = [
    path("list/", views.StudentEnrollmentListView.as_view(), name="enrollment_list"),
    path("create/", views.EnrollmentActionView.as_view(), name="enrollment_create"),
]
