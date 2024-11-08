from django.db import models
from django.apps import apps
from django.contrib.auth.models import User


class EmployeeCourse(models.Model):
    employee = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey('admin_app.Course', on_delete=models.CASCADE)
    date_assigned = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.employee.username} - {self.course.name}"
