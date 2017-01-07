from django.conf.urls import url

from . import views
from . import api

urlpatterns = [
    url(r'^home/$', views.home, name='home'),
    url(r'^model/(?P<id>\d+)/$', views.model, name='model'),
    url(r'^my_models/', views.my_models, name='my_models'),
    url(r'^calibration/(?P<id>\d+)/$', views.calibration, name='calibration'),
    url(r'^my_models_settings/(?P<id>\d+)/$', views.my_models_settings, name='my_models_settings'),

    # API URLs
    url(r'^api/home/get/$', api.home_info, name='home_info'),
    url(r'^api/model/get/(?P<id>\d+)/$', api.model_info, name='model_info'),
    url(r'^api/nodes/get/(?P<id>\d+)/$', api.nodes_info, name='nodes_info'),
    url(r'^api/model/calibrate/(?P<id>\d+)/$', api.model_calibrate, name='model_calibrate'),
    url(r'^api/calibration/get/(?P<id>\d+)/$', api.calibration_info, name='calibration_info'),
    url(r'^api/my_models/get/$', api.my_models_info, name='my_models_info'),
    url(r'^api/my_models/add/(?P<id>\d+)/$', api.add_model, name='add_model'),
    url(r'^api/my_models/remove/(?P<id>\d+)/$', api.remove_model, name='remove_model'),
    url(r'^api/my_models/copy/(?P<id>\d+)/$', api.copy_model, name='copy_model'),
    url(r'^api/my_models/set/description/(?P<id>\d+)/$', api.my_model_update_description, name='set_description'),
]
