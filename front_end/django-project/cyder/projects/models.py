from django.db import models
from cyder.models.models import Model
import json
from celery.result import AsyncResult
import sim_worker.celery
import sim_worker.tasks

class ProjectException(Exception):
    pass

# Create your models here.
class Project(models.Model):
    name = models.CharField(max_length=50)
    task_id = models.CharField(max_length=70, blank=True)
    stage = models.CharField(max_length=20, default="Modification")
    status = models.CharField(max_length=20, default="NA")
    settings = models.TextField(default="null")
    config = models.TextField(default="null")
    results = models.TextField(default="null")
    def __str__(self):
        return self.name

    def __init__(self, *args, **kwargs):
        if 'settings' in kwargs:
            kwargs['settings'] = json.dumps(kwargs['settings'])
        if 'config' in kwargs:
            kwargs['config'] = json.dumps(kwargs['config'])
        if 'results' in kwargs:
            kwargs['results'] = json.dumps(kwargs['results'])
        super(Project, self).__init__(*args, **kwargs)
        self.old_settings = self.settings
        self.settings = json.loads(self.settings)
        self.config = json.loads(self.config)
        self.results = json.loads(self.results)

    def save(self, *args, **kwargs):
        settings = self.settings
        self.settings = json.dumps(self.settings, separators=(',',':'))
        config = self.config
        self.config = json.dumps(self.config, separators=(',',':'))
        results = self.results
        self.results = json.dumps(self.results, separators=(',',':'))
        if self.old_settings != self.settings:
            self.old_settings = self.settings
            self.stage = "Modification"
            self.status = "NA"
        super(Project, self).save(*args, **kwargs)
        self.settings = settings
        self.config = config
        self.results = results

    def revoke(self):
        task = AsyncResult(self.task_id, app=sim_worker.celery.app)
        task.revoke(terminate=True)
        task.forget()
        if self.stage == "Configuration":
            self.stage = "Modification"
            self.status = "NA"
        elif self.stage == "Simulation":
            self.stage = "Configuration"
            self.status = "Success"
        self.save()

    def run_config(self):
        if self.status == "Started" or self.status == "Pending":
            raise ProjectException("Can't configure a project when it is currently in " + self.stage)
        task = sim_worker.tasks.run_configuration.delay(self.id, self.settings)
        self.task_id = task.id
        self.stage = "Configuration"
        self.status = "Pending"
        self.save()

    def run_sim(self):
        if self.status == "Started" or self.status == "Pending":
            raise ProjectException("Can't run a simulation on a project when it is currently in " + self.stage)
        if self.stage != "Simulation" and (not (self.stage == "Configuration" and self.status == "Success")):
            raise ProjectException("A succeed configuration must be performed before running a simulation")
        task = sim_worker.tasks.run_simulation.delay(self.id)
        self.task_id = task.id
        self.stage = "Simulation"
        self.status = "Pending"
        self.save()