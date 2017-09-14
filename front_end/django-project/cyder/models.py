from django.db import models

# Create your models here.
class Model(models.Model):
	filename = models.CharField(max_length=50, null=True, blank=True)
#	lat = models.FloatField(null=True, blank=True)
#	lon = models.FloatField(null=True, blank=True)
#	breaker_name = models.CharField(max_length=50, null=True, blank=True)
#	city = models.CharField(max_length=50, null=True, blank=True)
#	area = models.CharField(max_length=50, null=True, blank=True)
#	region = models.CharField(max_length=50, null=True, blank=True)
#	zip_code = models.CharField(max_length=50, null=True, blank=True)
#	version = models.CharField(max_length=50, null=True, blank=True)
#	upmu_location = models.CharField(max_length=50, null=True, blank=True)

#	def __str__(self):
#		return u"%s %s" % (self.region, self.filename)


class Node(models.Model):
	model = models.ForeignKey(Model, null=True, blank=True)
	node_id = models.CharField(max_length=50, null=True, blank=True)
	section_id = models.CharField(max_length=50, null=True, blank=True)
	longitude = models.FloatField(null=True, blank=True)
	latitude = models.FloatField(null=True, blank=True)
	class Meta:
		unique_together = ('model', 'node_id',)

class Device(models.Model):
	model = models.ForeignKey(Model, null=True, blank=True)
	device_number = models.CharField(max_length=50, null=True, blank=True)
	device_type = models.CharField(max_length=50, null=True, blank=True)
	device_type_id = models.CharField(max_length=50, null=True, blank=True)
	section_id = models.CharField(max_length=50, null=True, blank=True)
	distance = models.FloatField(null=True, blank=True)
	latitude = models.FloatField(null=True, blank=True)
	longitude = models.FloatField(null=True, blank=True)
	from_node_id = models.CharField(max_length=50, null=True, blank=True)
	to_node_id = models.CharField(max_length=50, null=True, blank=True)
	class Meta:
		unique_together = ('model', 'device_number',)
