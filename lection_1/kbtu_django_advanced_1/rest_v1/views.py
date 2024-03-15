import json

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from rest_v2 import models


@method_decorator(csrf_exempt, name="dispatch")
class StudentListView(View):
    def get(self, request, *args, **kwargs):
        objects = models.Student.objects.all()
        serialized_data = [{"id": obj.id, "name": obj.name, "age": obj.age, "sex": obj.sex} for obj in objects]
        return JsonResponse(serialized_data, safe=False)

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body.decode("utf-8"))

        obj = models.Student.objects.create(
            name=data.get("name", ""),
            age=data.get("age", ""),
            sex=data.get("sex", ""),
        )

        serialized_data = {"id": obj.id, "name": obj.name, "age": obj.age, "sex": obj.sex}
        return JsonResponse(serialized_data, status=201)


@method_decorator(csrf_exempt, name="dispatch")
class StudentDetailView(View):
    def get(self, request, *args, **kwargs):
        obj = get_object_or_404(models.Student, pk=kwargs["pk"])
        serialized_data = {"id": obj.id, "name": obj.name, "age": obj.age, "sex": obj.sex}
        return JsonResponse(serialized_data)

    def put(self, request, *args, **kwargs):
        obj = get_object_or_404(models.Student, pk=kwargs["pk"])
        data = json.loads(request.body.decode("utf-8"))

        obj.name = data.get("name", obj.name)
        obj.age = data.get("age", obj.age)
        obj.sex = data.get("sex", obj.sex)
        obj.save()

        serialized_data = {"id": obj.id, "name": obj.name, "age": obj.age, "sex": obj.sex}
        return JsonResponse(serialized_data)

    def delete(self, request, *args, **kwargs):
        obj = get_object_or_404(models.Student, pk=kwargs["pk"])
        print(len(kwargs))
        obj.delete()
        return JsonResponse({"message": "Object deleted successfully"}, status=204)
