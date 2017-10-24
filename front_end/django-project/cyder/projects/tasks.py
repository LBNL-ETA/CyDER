from celery_beat.celery import app
from celery.result import AsyncResult
from celery.states import PENDING, STARTED, SUCCESS, FAILURE
from .models import *
from django.db.models import Q

@app.task
def retrieve_projects_result():
    projectsInSim = Project.objects.filter(Q(status="Pending") | Q(status="Started"))
    for project in projectsInSim:
        result = AsyncResult(project.task_id)
        if result.status == PENDING:
            project.status = "Pending"
        elif result.status == STARTED:
            project.status = "Started"
        elif result.status == SUCCESS:
            project.status = "Success"
            project.result = result.get()
        elif result.status == FAILURE:
            project.status = "Failed"
        else:
            project.status = "NeedSim"
    project.save()
    return
