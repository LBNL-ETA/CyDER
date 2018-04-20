from rest_framework import serializers
from .models import Project, SimulationResult, ComponentResult
import json

class JSONField(serializers.JSONField):
    '''
    Field that output native json and store data into json string internally
    '''
    def __init__(self, *args, **kwargs):
        super(JSONField, self).__init__(*args, **kwargs)

    def to_internal_value(self, data):
        return json.dumps(super(JSONField, self).to_internal_value(data))

    def to_representation(self, value):
        return json.loads(super(JSONField, self).to_representation(value))

class ProjectSerializer(serializers.ModelSerializer):
    settings = JSONField()
    config = JSONField(read_only=True)
    results = JSONField(read_only=True)
    class Meta:
        model = Project
        exclude = ['task_id']
        read_only_fields = ['config', 'results', 'stage', 'status']

class SimulationResultSerializer(serializers.ModelSerializer):
    results = JSONField(read_only=True)
    class Meta:
        model = SimulationResult
        read_only_fields = ['project', 'date', 'results']

class ComponentResultSerializer(serializers.ModelSerializer):
    results = JSONField(read_only=True)
    class Meta:
        model = ComponentResult
        read_only_fields = ['project', 'component', 'results']