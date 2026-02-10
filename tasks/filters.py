import django_filters
from .models import Task


class TaskFilter(django_filters.FilterSet):
    deadline = django_filters.DateFromToRangeFilter()

    class Meta:
        model = Task
        fields = ['status', 'deadline']
