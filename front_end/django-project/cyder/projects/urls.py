from django.urls import path
from . import views

urlpatterns = [
    path('', views.projects, name='projects'),
    path('create/', views.create, name='createproject'),
    path('edit/<int:project_id>/', views.edit, name='editproject'),
    path('results/<int:project_id>/', views.results, name='projectresults'),
    path('config/<int:project_id>/', views.config, name='projectconfig'),
]
