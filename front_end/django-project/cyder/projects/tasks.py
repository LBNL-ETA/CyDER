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
        tasks = json.loads(project.task_id)
        if tasks:
            status = "Success"
            for task_id in tasks:
                task = AsyncResult(task_id, app=sim_worker.celery.app)
                if task.status == PENDING:
                    status = "Pending"
                elif task.status == STARTED:
                    status = "Started"
                elif task.status == SUCCESS:
                    if project.stage == "Configuration":
                        project.config = json.dumps(task.result, separators=(',',':'))
                    elif project.stage == "Detail Configuration":
                        project.config_detail = json.dumps(task.result, separators=(',',':'))
                    elif project.stage == "Simulation":
                        if (len(SimulationResult.objects.filter(Q(project=project)))<=len(tasks)) and (not SimulationResult.objects.filter(Q(project=project) & Q(task=task))) :
                            date=task.result['date']
                            results=json.dumps(task.result['results'], separators=(',',':'))
                            SimResult=SimulationResult(project=project, task=task,  date=date, results=results )
                            SimResult.save()
                        elif len(SimulationResult.objects.filter(Q(project=project)))==len(tasks):
                            getComponentResults()
                elif task.status == FAILURE:
                    project.status = "Failure"
            project.status = status
        project.save()


def getComponentResults(): 
    
    return