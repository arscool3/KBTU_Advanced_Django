from rest_framework import serializers

from . import models


class StudentSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)

    class Meta:
        model = models.Student
        fields = "__all__"
