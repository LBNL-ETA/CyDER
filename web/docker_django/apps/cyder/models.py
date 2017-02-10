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

    def __str__(self):
        return u"%s %s" % (self.region, self.filename)


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


class Project(models.Model):
    """docstring for Project."""
    user = models.ForeignKey(User, null=True, blank=True)
    name = models.CharField(max_length=50, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    last_modified = models.DateTimeField(null=True, blank=True)
    in_progress = models.BooleanField(default=False)
    result_available = models.BooleanField(default=False)
    status = models.TextField(null=True, blank=True)

    def __str__(self):
        return u"%s avail. result: %s" % (self.user, self.result_available)


class ProjectModels(models.Model):
    """docstring for Project."""
    project = models.ForeignKey(Project, null=True, blank=True)
    model = models.ForeignKey(Model, null=True, blank=True)

    def __str__(self):
        return u"%s %s" % (self.project, self.model)


class ElectricVehicleScenario(models.Model):
    """docstring for ElectricVehicleScenario."""
    project_model = models.OneToOneField(ProjectModels, null=True, blank=True)
    nb_vehicles = models.IntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=False)


class NodeResult(models.Model):
    """docstring for NodeResult."""
    project_model = models.ForeignKey(ProjectModels, null=True, blank=True)
    node_id = models.CharField(max_length=50, null=True, blank=True)
    distance = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    voltage_A = models.FloatField(null=True, blank=True)
    voltage_B = models.FloatField(null=True, blank=True)
    voltage_C = models.FloatField(null=True, blank=True)


class CurrentCalibration(models.Model):
    """docstring for CalibrationData."""
    model = models.OneToOneField(Model, null=True, blank=True)
    impedance_real = models.FloatField(null=True, blank=True)
    impedance_imag = models.FloatField(null=True, blank=True)


class CalibrationHistory(models.Model):
    """docstring for CalibrationHistory"""
    model = models.ForeignKey(Model, null=True, blank=True)
    date = models.DateTimeField(null=True, blank=True)
    updated = models.BooleanField(default=False)
    calibration_algorithm = models.TextField(null=True, blank=True)

    def __str__(self):
        return u"%s %s" % (self.model.region, self.date)


class CalibrationResult(models.Model):
    """docstring for CalibrationData."""
    calibration = models.OneToOneField(CalibrationHistory, null=True, blank=True)
    impedance_real = models.FloatField(null=True, blank=True)
    impedance_imag = models.FloatField(null=True, blank=True)


class CalibrationData(models.Model):
    """docstring for CalibrationData."""
    calibration = models.OneToOneField(CalibrationHistory, null=True, blank=True)

    # uPMU data at the feeder
    p_a_feeder = models.FloatField(null=True, blank=True)
    p_b_feeder = models.FloatField(null=True, blank=True)
    p_c_feeder = models.FloatField(null=True, blank=True)
    q_a_feeder = models.FloatField(null=True, blank=True)
    q_b_feeder = models.FloatField(null=True, blank=True)
    q_c_feeder = models.FloatField(null=True, blank=True)
    volt_mag_a_feeder = models.FloatField(null=True, blank=True)
    volt_mag_b_feeder = models.FloatField(null=True, blank=True)
    volt_mag_c_feeder = models.FloatField(null=True, blank=True)
    volt_ang_a_feeder = models.FloatField(null=True, blank=True)
    volt_ang_b_feeder = models.FloatField(null=True, blank=True)
    volt_ang_c_feeder = models.FloatField(null=True, blank=True)
    v1_real_feeder = models.FloatField(null=True, blank=True)
    v1_imag_feeder = models.FloatField(null=True, blank=True)

    # uPMU data downstream
    p_a_downstream = models.FloatField(null=True, blank=True)
    p_b_downstream = models.FloatField(null=True, blank=True)
    p_c_downstream = models.FloatField(null=True, blank=True)
    q_a_downstream = models.FloatField(null=True, blank=True)
    q_b_downstream = models.FloatField(null=True, blank=True)
    q_c_downstream = models.FloatField(null=True, blank=True)
    volt_mag_a_downstream = models.FloatField(null=True, blank=True)
    volt_mag_b_downstream = models.FloatField(null=True, blank=True)
    volt_mag_c_downstream = models.FloatField(null=True, blank=True)
    volt_ang_a_downstream = models.FloatField(null=True, blank=True)
    volt_ang_b_downstream = models.FloatField(null=True, blank=True)
    volt_ang_c_downstream = models.FloatField(null=True, blank=True)
    v1_real_downstream = models.FloatField(null=True, blank=True)
    v1_imag_downstream = models.FloatField(null=True, blank=True)

    # Simulation results
    i1_real_sim = models.FloatField(null=True, blank=True)
    i1_imag_sim = models.FloatField(null=True, blank=True)
