from rest_framework import serializers
from django.db.models import Count
from . import models
import sys


class ModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Model
        fields = '__all__'


class NodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Node
        fields = '__all__'


class DevicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Devices
        fields = '__all__'


class DetailModelSerializer(serializers.ModelSerializer):
    devices = serializers.SerializerMethodField()

    class Meta:
        model = models.Model
        exclude = []

    def get_devices(self, obj):
        try:
            # Add the counts of the different devices
            devices = models.Devices.objects.filter(model=self.instance.id)
        except:
            return str(sys.exc_info()[0])
        return devices.values('device_type').order_by().annotate(count=Count('device_type')).order_by('count')
