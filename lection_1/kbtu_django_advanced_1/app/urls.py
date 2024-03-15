from app.views import add_student, index
from django.urls import path

urlpatterns = [
    path("", index, name="index"),
    path("add", add_student, name="add"),
]
