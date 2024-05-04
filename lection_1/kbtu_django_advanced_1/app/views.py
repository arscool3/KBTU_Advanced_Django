from app.forms import Student
from django.shortcuts import render

# Create your views here.

students = [
    "Zhanserik",
    "Arslan",
    "Askar",
    "Test",
]


def index(request):
    return render(request, "index.html", {"students": students})


def add_student(request):
    form = Student(request.POST)

    if request.method == "POST":
        if form.is_valid():
            student_name = form.cleaned_data["name"]
            students.append(student_name)
        else:
            raise Exception("No valid Student")

    return render(request, "form.html", {"form": form})
