from django.db import models

# Create your models here.
class Device(models.Model):
    device_number = models.CharField(max_length=50, null=True, blank=True)
    device_type = models.CharField(max_length=50, null=True, blank=True)
    device_type_id = models.CharField(max_length=50, null=True, blank=True)
    section_id = models.CharField(max_length=50, null=True, blank=True)
    distance = models.FloatField(null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
