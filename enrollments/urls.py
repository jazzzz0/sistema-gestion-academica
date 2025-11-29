from django.urls import path
from . import views
from enrollments.views import EnrollmentAdminListView

app_name = "enrollments"

urlpatterns = [
    path("", views.inicio, name="inicio"),
    path("my-enrollments/", views.MyEnrollmentListView.as_view(), name="my_enrollments"),
    path("unenroll/<int:pk>/", views.EnrollmentDropView.as_view(), name="enrollment_drop"),
    path("admin-list/", EnrollmentAdminListView.as_view(), name="enrollment_admin_list"),

]
