from django.db import models
from ..grid_models.models import Model

# Create your models here.
class Project(models.Model):
    name = models.CharField(max_length=50)
    task_id = models.CharField(max_length=70, blank=True)
    model = models.ForeignKey(Model, null=True, blank=True)
    status = models.CharField(max_length=10)
    def __str__(self):
        return self.name
