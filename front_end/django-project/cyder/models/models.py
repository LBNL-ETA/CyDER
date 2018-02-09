from django.db import models

# Create your models here.
class Model(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    def __str__(self):
        return self.name

class Node(models.Model):
    model = models.ForeignKey(Model, null=True, blank=True, on_delete=models.CASCADE)
    node_id = models.CharField(max_length=50, null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    VA = models.FloatField(null=True, blank=True)
    VB = models.FloatField(null=True, blank=True)
    VC = models.FloatField(null=True, blank=True)
    class Meta:
        unique_together = ('model', 'node_id',)
    def __str__(self):
        return self.node_id

class Section(models.Model):
    model = models.ForeignKey(Model, null=True, blank=True, on_delete=models.CASCADE)
    section_id = models.CharField(max_length=50, null=True, blank=True)
    from_node = models.ForeignKey(Node, null=True, blank=True, on_delete=models.CASCADE, related_name='origin_sections')
    to_node = models.ForeignKey(Node, null=True, blank=True, on_delete=models.CASCADE, related_name='end_sections')
    class Meta:
        unique_together = ('model', 'section_id',)
    def __str__(self):
        return self.section_id

class Device(models.Model):
    model = models.ForeignKey(Model, null=True, blank=True, on_delete=models.CASCADE)
    device_number = models.CharField(max_length=50, null=True, blank=True)
    device_type = models.IntegerField()
    section = models.ForeignKey(Section, null=True, blank=True, on_delete=models.CASCADE)
    distance = models.FloatField(null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    class Meta:
        unique_together = ('model', 'device_number', 'device_type',)
    def __str__(self):
        return self.device_number

class Load(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    SpotKWA = models.FloatField(null=True, blank=True)
    SpotKWB = models.FloatField(null=True, blank=True)
    SpotKWC = models.FloatField(null=True, blank=True)

class PV(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    PVActiveGeneration = models.FloatField(null=True, blank=True)
