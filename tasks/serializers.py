from rest_framework import serializers
from django.utils import timezone
from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.email')

    class Meta:
        model = Task
        fields = (
            'id',
            'title',
            'description',
            'status',
            'deadline',
            'owner',
            'created_at',
            'updated_at',
        )

    def validate_title(self, value):
        if not value.strip():
            raise serializers.ValidationError("Title пустой болбошу керек")
        return value

    def validate_description(self, value):
        if len(value) < 10:
            raise serializers.ValidationError(
                "Description минимум 10 символ болушу керек"
            )
        return value

    def validate_deadline(self, value):
        if value < timezone.now().date():
            raise serializers.ValidationError(
                "Deadline өткөн күн болбошу керек"
            )
        return value

    def validate_status(self, value):
        statuses = [choice[0] for choice in Task.STATUS_CHOICES]
        if value not in statuses:
            raise serializers.ValidationError("Неверный статус")
        return value
