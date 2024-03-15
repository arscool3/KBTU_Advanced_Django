from django.urls import path

from . import views

urlpatterns = [
    path("students/", views.StudentListView.as_view(), name="student-list"),
    path("students/<pk>/", views.StudentDetailView.as_view(), name="student-detail"),
]
