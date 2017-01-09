from django.db import models
from django.contrib.auth.models import User


class Model(models.Model):
    """docstring for Model."""
    filename = models.CharField(max_length=50, null=True, blank=True)
    lat = models.FloatField(null=True, blank=True)
    lon = models.FloatField(null=True, blank=True)
    breaker_name = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    area = models.CharField(max_length=50, null=True, blank=True)
    region = models.CharField(max_length=50, null=True, blank=True)
    zip_code = models.CharField(max_length=50, null=True, blank=True)
    version = models.CharField(max_length=50, null=True, blank=True)
    upmu_location = models.CharField(max_length=50, null=True, blank=True)


class Node(models.Model):
    """docstring for Node."""
    model = models.ForeignKey(Model, null=True, blank=True)
    node_id = models.CharField(max_length=50, null=True, blank=True)
    section_id = models.CharField(max_length=50, null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)


class Devices(models.Model):
    """docstring for devices"""
    model = models.ForeignKey(Model, null=True, blank=True)
    device_number = models.CharField(max_length=50, null=True, blank=True)
    device_type = models.CharField(max_length=50, null=True, blank=True)
    device_type_id = models.CharField(max_length=50, null=True, blank=True)
    section_id = models.CharField(max_length=50, null=True, blank=True)
    distance = models.FloatField(null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)


class UserModel(models.Model):
    """docstring for UserModel."""
    user = models.ForeignKey(User, null=True, blank=True)
    model = models.ForeignKey(Model, null=True, blank=True)
    name = models.CharField(max_length=50, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    simulation_date = models.DateTimeField(null=True, blank=True)


class CurrentCalibration(models.Model):
    """docstring for CalibrationData."""
    model = models.OneToOneField(Model, null=True, blank=True)
    impedance_a = models.FloatField(null=True, blank=True)
    impedance_b = models.FloatField(null=True, blank=True)
    impedance_c = models.FloatField(null=True, blank=True)


class CalibrationHistory(models.Model):
    """docstring for CalibrationHistory"""
    model = models.ForeignKey(Model, null=True, blank=True)
    date = models.DateTimeField(null=True, blank=True)
    updated = models.BooleanField(default=False)
    calibration_algorithm = models.TextField(null=True, blank=True)


class CalibrationResult(models.Model):
    """docstring for CalibrationData."""
    calibration = models.OneToOneField(CalibrationHistory, null=True, blank=True)
    impedance_a = models.FloatField(null=True, blank=True)
    impedance_b = models.FloatField(null=True, blank=True)
    impedance_c = models.FloatField(null=True, blank=True)


class CalibrationData(models.Model):
    """docstring for CalibrationData."""
    calibration = models.OneToOneField(CalibrationHistory, null=True, blank=True)
    p_a = models.FloatField(null=True, blank=True)
    p_b = models.FloatField(null=True, blank=True)
    p_c = models.FloatField(null=True, blank=True)
    q_a = models.FloatField(null=True, blank=True)
    q_b = models.FloatField(null=True, blank=True)
    q_c = models.FloatField(null=True, blank=True)
    voltage_a = models.FloatField(null=True, blank=True)
    voltage_b = models.FloatField(null=True, blank=True)
    voltage_c = models.FloatField(null=True, blank=True)
