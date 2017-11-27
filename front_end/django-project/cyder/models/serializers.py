from rest_framework import serializers
from cyder.grid_models.models import *

class ModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Model
        exclude = ['id']

class NodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Node
        exclude = ['id', 'model']

class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        exclude = ['id', 'model']

class LoadSerializer(serializers.ModelSerializer):
    device_number = serializers.CharField(source='device.device_number', read_only=True)
    class Meta:
        model = Load
        exclude = ['id', 'device']
