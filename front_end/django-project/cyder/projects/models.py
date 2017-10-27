from django.db import models
from ..grid_models.models import Model

# Create your models here.
class Project(models.Model):
    name = models.CharField(max_length=50)
    task_id = models.CharField(max_length=70, blank=True)
    status = models.CharField(max_length=10, default="NeedSim")
    settings = models.TextField(blank=True)
    results = models.TextField(blank=True)
    def __str__(self):
        return self.name

    def __init__(self, *args, **kwargs):
        super(Project, self).__init__(*args, **kwargs)
        self.old_settings = self.settings

    def save(self, *args, **kwargs):
        if self.old_settings != self.settings:
            self.status = "NeedSim"
        super(Project, self).save(*args, **kwargs)
