from django.urls import path
from .views import StudentList, StudentDetail

urlpatterns = [
    path('students/', StudentList.as_view(), name='student-list'),
    path('students/<int:pk>/', StudentDetail.as_view(), name='student-detail'),
]

