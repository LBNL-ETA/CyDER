from django.conf.urls import url

from . import views
from . import api

urlpatterns = [
    url(r'^home/$', views.home, name='home'),
    url(r'^model/(?P<id>\d+)/$', views.model, name='model'),
    url(r'^api/home/get/$', api.home_info, name='home_info'),
    url(r'^api/model/get/(?P<id>\d+)/$', api.model_info, name='model_info'),
]
