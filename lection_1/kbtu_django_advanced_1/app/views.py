from django.shortcuts import render, redirect

from app1.forms import Student

# Create your views here.

students = [
    {'name': 'Zh', 'age': 25, 'sex': 'male'},
    {'name': 'A', 'age': 22, 'sex': 'male'},
    {'name': 'B', 'age': 23, 'sex': 'male'},
    {'name': 'C', 'age': 20, 'sex': 'female'},
]


def index(request):
    return render(request, 'index.html', {
        'students': students
    })


def add_student(request):
    form = Student(request.POST)
    if request.method == "POST":
        if form.is_valid():
            student_data = {
                'name': form.cleaned_data['name'],
                'age': form.cleaned_data['age'],
                'sex': form.cleaned_data['sex'],
            }
            students.append(student_data)
            return redirect('index')
        else:
            raise Exception("Error")

    return render(request, 'form.html', {'form': form})


def update_student(request, index):
    if request.method == "POST":
        form = Student(request.POST)
        if form.is_valid():
            students[index] = {
                'name': form.cleaned_data['name'],
                'age': form.cleaned_data['age'],
                'sex': form.cleaned_data['sex'],
            }
            return redirect('index')
    else:
        student_data = students[index]
        form = Student(initial=student_data)

    return render(request, 'update.html', {'form': form, 'index': index})


def delete_student(request, index):
    student_data = students[index]
    if request.method == 'POST':
        del students[index]
        return redirect('index')

    return render(request, 'delete.html', {'student': student_data, 'index': index})


