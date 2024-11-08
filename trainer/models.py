from django.db import models
from django.contrib.auth.models import User
from django.apps import apps  # Make sure to import the Course model

class Trainer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    assigned_courses = models.ManyToManyField('admin_app.Course', related_name="trainers")

    def __str__(self):
        return self.user.get_full_name()
