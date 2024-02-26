import uuid

from django.db import models

from . import choices


class Student(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    sex = models.CharField(max_length=7, choices=choices.SexChoices.choices, null=False, blank=False)

    def __str__(self):
        return f"{self.id} - {self.name}"
