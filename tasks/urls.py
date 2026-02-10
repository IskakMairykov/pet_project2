from django.urls import path
from .views import task_list_view, edit_task_view, delete_task_view

urlpatterns = [
    path('tasks/', task_list_view, name='task_list'),
    path('tasks/edit/<int:task_id>/', edit_task_view, name='edit_task'),
    path('tasks/delete/<int:task_id>/', delete_task_view, name='delete_task'),
]
