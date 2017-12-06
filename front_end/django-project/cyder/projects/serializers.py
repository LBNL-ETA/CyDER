from rest_framework import serializers
from .models import Project

class ProjectSerializer(serializers.ModelSerializer):
    settings = serializers.JSONField()
    config = serializers.JSONField(read_only=True)
    results = serializers.JSONField(read_only=True)
    class Meta:
        model = Project
        exclude = ['task_id']
        read_only_fields = ['config', 'results', 'stage', 'status']
