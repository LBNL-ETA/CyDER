from celery_beat.celery import app
from celery.result import AsyncResult
from celery.states import PENDING, STARTED, SUCCESS, FAILURE
from .models import *
from django.db.models import Q
import json

import sim_worker.celery

@app.task
def retrieve_projects_result():
    projectsInWork = Project.objects.filter(Q(status="Pending") | Q(status="Started"))
    for project in projectsInWork:
        task = AsyncResult(project.task_id, app=sim_worker.celery.app)
        if task.status == PENDING:
            project.status = "Pending"
        elif task.status == STARTED:
            project.status = "Started"
        elif task.status == SUCCESS:
            project.status = "Success"
            if project.stage == "Configuration":
                project.config = json.dumps(task.result, separators=(',',':'))
            elif project.stage == "Detail Configuration":
                project.config_detail = json.dumps(task.result, separators=(',',':'))
            elif project.stage == "Simulation":
                project.results = json.dumps(task.result, separators=(',',':'))
        elif task.status == FAILURE:
            project.status = "Failure"
        project.save()
