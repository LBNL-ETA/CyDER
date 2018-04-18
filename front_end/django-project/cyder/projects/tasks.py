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
            if project.stage == "Configuration":
                project.config = json.dumps(task.result, separators=(',',':'))
                project.status = "Success"
            elif project.stage == "Detail Configuration":
                project.config_detail = json.dumps(task.result, separators=(',',':'))
                project.status = "Success"
            elif project.stage == "Simulation":
                settings=json.loads(project.settings)
                if settings['nextSimDay']==settings['simDaysList'][0]:
                    temp={}
                    temp[settings['nextSimDay']]=json.loads(task.result)
                    project.results = json.dumps(temp,  indent=4, separators=(',',':'))
                    settings['nextSimDay']=settings['simDaysList'][settings['simDaysList'].index(settings['nextSimDay'])+1]
                    project.settings=json.dumps(settings)
                    project.saveBis()
                    task = sim_worker.tasks.run_simulation.delay(project.id, settings, settings['nextSimDay'])
                    project.task_id = task.id
                elif settings['nextSimDay']==settings['simDaysList'][len(settings['simDaysList'])-1]:
                    temp=json.loads(project.results)
                    temp[settings['nextSimDay']]=json.loads(task.result)
                    project.results = json.dumps(temp,  indent=4, separators=(',',':'))
                    settings['nextSimDay']= ''
                    project.settings=json.dumps(settings)
                else:
                    temp=json.loads(project.results)
                    temp[settings['nextSimDay']]=json.loads(task.result)
                    project.results = json.dumps(temp, indent=4, separators=(',',':'))
                    settings['nextSimDay']=settings['simDaysList'][settings['simDaysList'].index(settings['nextSimDay'])+1]
                    project.settings=json.dumps(settings)
                    project.saveBis()
                    task = sim_worker.tasks.run_simulation.delay(project.id, settings, settings['nextSimDay'])
                    project.task_id = task.id
        elif task.status == FAILURE:
            project.status = "Failure"
        project.save()
