from rest_framework import serializers
from cyder.grid_models.models import Model, Node, Device

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
