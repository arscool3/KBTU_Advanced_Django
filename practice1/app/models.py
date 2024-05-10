from django.db import models

# Create your models here.
class Student(models.Model):
    name = models.CharField(max_length=100, null=True);
    age = models.IntegerField()
    sex = models.CharField(max_length=50)

