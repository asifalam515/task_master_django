
from django.db import models
from django.contrib.auth.models import User

# class Category(models.Model):
#     name = models.CharField(max_length=255)

#     def __str__(self):
#         return self.name
class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    due_date = models.DateField(null=True, blank=True)
    priority = models.IntegerField(default=0, choices=[(i, i) for i in range(9)])
    category = models.CharField(max_length=100)
    status = models.BooleanField(default=False)  # False for incomplete, True for completed

    def __str__(self):
        return self.title


