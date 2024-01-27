from django.contrib import admin
from django.urls import path

from app.views import students_list, student_details

urlpatterns = [
    path("", students_list),
    path("<int:id>", student_details),
]
