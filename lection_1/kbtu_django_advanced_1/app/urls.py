from django.contrib import admin
from django.urls import path

from app1.views import index, add_student, update_student, delete_student

urlpatterns = [
    path("", index, name='index'),
    path("add/", add_student, name='add'),
    path('update/<int:index>/', update_student, name='update_student'),
    path('delete/<int:index>/', delete_student, name='delete_student'),

]
