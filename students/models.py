from django.db import models


class Student(models.Model):
    student_id = models.CharField(max_length=30, unique=True)
    name = models.CharField(max_length=100)
    course = models.CharField(max_length=100)
    scores = models.JSONField(default=list, blank=True)

    def __str__(self):
        return self.student_id + " - " + self.name