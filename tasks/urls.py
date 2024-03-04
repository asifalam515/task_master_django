# urls.py
from django.urls import path
from .views import task_list, create_task, edit_task, delete_task, mark_completed

urlpatterns = [
    path('tasks/', task_list, name='task_list'),
    path('tasks/create/', create_task, name='create_task'),
    path('tasks/<int:task_id>/edit/', edit_task, name='edit_task'),
    path('tasks/<int:task_id>/delete/', delete_task, name='delete_task'),
    path('tasks/<int:task_id>/mark_completed/', mark_completed, name='mark_completed'),
]
