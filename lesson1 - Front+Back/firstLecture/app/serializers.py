from rest_framework import serializers
from app.models import Student


# model serializer
class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'
