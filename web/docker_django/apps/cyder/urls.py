from django.conf.urls import url

from . import views
from . import api

urlpatterns = [
    url(r'^home/$', views.home, name='home'),
    url(r'^model/(?P<id>\d+)/$', views.model, name='model'),
    url(r'^my_models/', views.my_models, name='my_models'),
    url(r'^calibration/(?P<id>\d+)/$', views.calibration, name='calibration'),
    url(r'^api/home/get/$', api.home_info, name='home_info'),
    url(r'^api/model/get/(?P<id>\d+)/$', api.model_info, name='model_info'),
    url(r'^api/model/update/(?P<id>\d+)/$', api.model_update, name='model_update'),
    url(r'^api/calibration/get/(?P<id>\d+)/$', api.calibration_info, name='calibration_info'),
    url(r'^api/my_models/get/$', api.my_models_info, name='my_models_info'),
    url(r'^api/my_models/add/(?P<id>\d+)/$', api.add_model, name='add_model'),
]
