from django.db import models
from ..grid_models.models import Model
import json

# Create your models here.
class Project(models.Model):
    name = models.CharField(max_length=50)
    task_id = models.CharField(max_length=70, blank=True)
    status = models.CharField(max_length=10, default="NeedSim")
    settings = models.TextField(default="null")
    results = models.TextField(default="null")
    def __str__(self):
        return self.name

    def __init__(self, *args, **kwargs):
        if 'settings' in kwargs:
            kwargs['settings'] = json.dumps(kwargs['settings'])
        if 'results' in kwargs:
            kwargs['results'] = json.dumps(kwargs['results'])
        super(Project, self).__init__(*args, **kwargs)
        self.old_settings = self.settings
        self.settings = json.loads(self.settings)
        self.results = json.loads(self.results)

    def save(self, *args, **kwargs):
        settings = self.settings
        self.settings = json.dumps(self.settings, separators=(',',':'))
        results = self.results
        self.results = json.dumps(self.results, separators=(',',':'))
        if self.old_settings != self.settings:
            self.old_settings = self.settings
            self.status = "NeedSim"
        super(Project, self).save(*args, **kwargs)
        self.settings = settings
        self.results = results
