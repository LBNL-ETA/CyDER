from celery_beat.celery import app
from celery.result import AsyncResult
from celery.states import PENDING, STARTED, SUCCESS, FAILURE
from .models import *
from django.db.models import Q

import sim_worker.celery

@app.task
def retrieve_projects_result():
    projectsInSim = Project.objects.filter(Q(status="Pending") | Q(status="Started"))
    for project in projectsInSim:
        task = AsyncResult(project.task_id, app=sim_worker.celery.app)
        if task.status == PENDING:
            project.status = "Pending"
        elif task.status == STARTED:
            project.status = "Started"
        elif task.status == SUCCESS:
            project.status = "Succeed"
            project.result = task.result
        elif task.status == FAILURE:
            project.status = "Failed"
        else:
            project.status = "NeedSim"
        project.save()
    return
