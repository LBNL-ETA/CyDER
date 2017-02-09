from __future__ import division
from rest_framework import serializers
from django.db.models import Count
from . import models
import traceback
import sys


class ActionSerializer(serializers.Serializer):
    options = serializers.CharField(max_length=200)
    description = serializers.CharField(max_length=200)


class ModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Model
        fields = '__all__'


class ElectricVehicleScenarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ElectricVehicleScenario
        fields = '__all__'


class UserModelSerializer(serializers.ModelSerializer):
    model_region = serializers.SerializerMethodField()

    class Meta:
        model = models.UserModel
        fields = '__all__'

    def get_model_region(self, obj):
        try:
            temp = models.Model.objects.filter(id=obj.model.id)
            regions = [value.region for value in temp]
        except:
            return str(traceback.format_exc())
        return regions


class NodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Node
        fields = '__all__'


class NodeResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.NodeResult
        fields = '__all__'


class DevicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Devices
        fields = '__all__'


class DetailModelSerializer(serializers.ModelSerializer):
    devices = serializers.SerializerMethodField()
    source_impedances = serializers.SerializerMethodField()

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

    def get_source_impedances(self, obj):
        try:
            # Get the history of calibrations
            history = list(models.CalibrationHistory.objects.filter(model=self.instance.id).values())

            for index, value in enumerate(history):
                # Get the Calibration results
                source_impedance = models.CalibrationResult.objects.filter(calibration=value['id'])
                if source_impedance:
                    history[index]['z_real'] = source_impedance[0].impedance_real
                    history[index]['z_imag'] = source_impedance[0].impedance_imag
                else:
                    history[index]['z_real'] = 0
                    history[index]['z_imag'] = 0
        except:
            return str(traceback.format_exc())
        return history


class CalibrationHistorySerializer(serializers.ModelSerializer):
    results = serializers.SerializerMethodField()
    class Meta:
        model = models.CalibrationHistory
        exclude = []

    def get_results(self, obj):
        try:
            # Get real and imaginary impedance values
            result = models.CalibrationResult.objects.get(
                calibration=obj.id)
        except:
            return str(traceback.format_exc())
        return {'impedance_real': result.impedance_real,
                'impedance_imag': result.impedance_imag}


class CalibrationDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CalibrationData
        exclude = ['calibration']


class SingleCalibrationHistorySerializer(serializers.ModelSerializer):
    results = serializers.SerializerMethodField()
    data = serializers.SerializerMethodField()
    class Meta:
        model = models.CalibrationHistory
        exclude = []

    def get_results(self, obj):
        try:
            # Get real and imaginary impedance values
            result = models.CalibrationResult.objects.get(
                calibration=self.instance.id)
        except:
            return str(traceback.format_exc())
        return {'impedance_real': result.impedance_real,
                'impedance_imag': result.impedance_imag}

    def get_data(self, obj):
        try:
            query = models.CalibrationData.objects.get(calibration_id=self.instance.id)
            serializer = CalibrationDataSerializer(query)
        except:
            return str(traceback.format_exc())
        return serializer.data
