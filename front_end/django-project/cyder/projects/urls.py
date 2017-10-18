from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.projects, name='projects'),
    #url(r'^createnew$', views.newproject, name='newproject'),
]
