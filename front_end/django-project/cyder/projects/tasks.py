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
        print(project)
        tasks = json.loads(project.task_id)
        print(tasks)
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
                        print(task.result)
                        date=task.result['date']
                        print(date)
                        results=json.dumps(task.result, separators=(',',':'))
                        simres=SimulationResult(project=project, date=date, results=results )
                        simres.save()
                elif task.status == FAILURE:
                    project.status = "Failure"
            project.status = status
        project.save()
