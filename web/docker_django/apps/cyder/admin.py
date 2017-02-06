from django.contrib import admin
from . import models


class ModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'region', 'filename')
    list_display_links = ('id', 'region')
    search_fields = ('region', 'area', 'city')
    list_per_page = 25


class CalibrationHistoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'model', 'date')
    list_display_links = ('id', 'model')
    search_fields = ('model__region', 'model__area', 'model__city', 'date')
    list_per_page = 25


class UserModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'model', 'name', 'description', 'last_modified')
    list_display_links = ('id', 'user', 'model')
    search_fields = ('model__region', 'model__area', 'model__city', 'user_username')
    list_per_page = 25


class ElectricVehicleScenarioAdmin(admin.ModelAdmin):
    list_display = ('id', 'usermodel', 'nb_vehicles', 'is_active')
    list_display_links = ('id', 'usermodel')
    search_fields = ('usermodel', 'nb_vehicles')
    list_per_page = 25


class CurrentCalibrationAdmin(admin.ModelAdmin):
    list_display = ('id', 'model')
    list_display_links = ('id', 'model')
    search_fields = ('model__region', 'model__area', 'model__city')
    list_per_page = 25


class CalibrationDataAdmin(admin.ModelAdmin):
    list_display = ('id', 'calibration')
    list_display_links = ('id', 'calibration')
    search_fields = ('calibration__model__region', 'calibration__model__area')
    list_per_page = 25


class CalibrationResultAdmin(admin.ModelAdmin):
    list_display = ('id', 'calibration', 'impedance_real', 'impedance_imag')
    list_display_links = ('id', 'calibration')
    search_fields = ('calibration__model__region', 'calibration__model__area', 'impedance_real')
    list_per_page = 25


class DevicesAdmin(admin.ModelAdmin):
    list_display = ('id', 'model', 'device_number', 'device_type', 'distance')
    list_display_links = ('id', 'model', 'device_number')
    search_fields = ('model__region', 'model__area', 'model__city', 'device_type', 'distance')
    list_per_page = 25


class NodeResultAdmin(admin.ModelAdmin):
    list_display = ('id', 'usermodel', 'node_id', 'voltage_A', 'voltage_B', 'voltage_C')
    list_display_links = ('id', 'usermodel')
    search_fields = ('usermodel', 'node_id')
    list_per_page = 25


# Register your models here.
admin.site.register(models.Model, ModelAdmin)
admin.site.register(models.Node)
admin.site.register(models.NodeResult, NodeResultAdmin)
admin.site.register(models.UserModel, UserModelAdmin)
admin.site.register(models.ElectricVehicleScenario, ElectricVehicleScenarioAdmin)
admin.site.register(models.CurrentCalibration, CurrentCalibrationAdmin)
admin.site.register(models.CalibrationHistory, CalibrationHistoryAdmin)
admin.site.register(models.CalibrationResult, CalibrationResultAdmin)
admin.site.register(models.CalibrationData, CalibrationDataAdmin)
admin.site.register(models.Devices, DevicesAdmin)
