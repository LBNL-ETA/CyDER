from rest_framework import serializers
from .models import Project

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        exclude = ['task_id']
        read_only_fields = ['result', 'status']
