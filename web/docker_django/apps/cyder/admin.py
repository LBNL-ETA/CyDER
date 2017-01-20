from django.contrib import admin
from . import models


class ModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'region', 'filename')
    list_display_links = ('id')
    search_fields = ('region', 'area', 'city')
    list_per_page = 25


class CalibrationHistoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'model', 'date')
    list_display_links = ('id', 'model')
    search_fields = ('model__region', 'model__area', 'model__city', 'date')
    list_per_page = 25


class UserModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'model', 'name', 'description', 'simulation_date')
    list_display_links = ('id')
    search_fields = ('model__region', 'model__area', 'model__city', 'user_username')
    list_per_page = 25


class CurrentCalibrationAdmin(admin.ModelAdmin):
    list_display = ('id', 'model')
    list_display_links = ('id')
    search_fields = ('model__region', 'model__area', 'model__city')
    list_per_page = 25


class CalibrationDataAdmin(admin.ModelAdmin):
    list_display = ('id', 'calibration', 'p_a', 'p_b', 'p_c')
    list_display_links = ('id')
    search_fields = ('calibration__model__region', 'calibration__model__area')
    list_per_page = 25

# Register your models here.
admin.site.register(models.Model, ModelAdmin)
admin.site.register(models.Node)
admin.site.register(models.UserModel, UserModelAdmin)
admin.site.register(models.CurrentCalibration, CurrentCalibrationAdmin)
admin.site.register(models.CalibrationHistory, CalibrationHistoryAdmin)
admin.site.register(models.CalibrationResult)
admin.site.register(models.CalibrationData, CalibrationDataAdmin)
