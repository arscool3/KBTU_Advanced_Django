from django.contrib import admin
from django.urls import path

from app.views import index, add_student

urlpatterns = [
    path("", index, name='index'),
    path("add", add_student, name='add'),
]
