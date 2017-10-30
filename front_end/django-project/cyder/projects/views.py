from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def projects(request):
    return render(request, 'cyder/projects/projects.html')

@login_required
def edit(request, project_id):
    return render(request, 'cyder/projects/edit.html', { 'project_id': project_id })

@login_required
def create(request):
    return render(request, 'cyder/projects/create.html')
