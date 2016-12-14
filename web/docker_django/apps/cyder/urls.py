from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^home/$', views.home, name='home'),
    url(r'^api/home/get/$', views.home_info, name='home_info'),
    url(r'^api/model/get/(?P<id>\d+)/$', views.model_info, name='model_info'),
]
