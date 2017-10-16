from django.db import models

# Create your models here.
class Model(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    def __str__(self):
        return self.name

class Node(models.Model):
    model = models.ForeignKey(Model, null=True, blank=True)
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
    model = models.ForeignKey(Model, null=True, blank=True)
    section_id = models.CharField(max_length=50, null=True, blank=True)
    from_node = models.ForeignKey(Node, null=True, blank=True, related_name='origin_sections')
    to_node = models.ForeignKey(Node, null=True, blank=True,related_name='end_sections')
    class Meta:
        unique_together = ('model', 'section_id',)
    def __str__(self):
        return self.section_id

class Device(models.Model):
    model = models.ForeignKey(Model, null=True, blank=True)
    device_number = models.CharField(max_length=50, null=True, blank=True)
    device_type = models.CharField(max_length=50, null=True, blank=True)
    section = models.ForeignKey(Section, null=True, blank=True)
    distance = models.FloatField(null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    class Meta:
        unique_together = ('model', 'device_number',)
    def __str__(self):
        return self.device_number
