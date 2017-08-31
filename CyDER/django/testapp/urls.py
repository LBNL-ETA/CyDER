from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^start_sim$', views.start_sim, name='start_sim'),
	url(r'^sim_started/(?P<taskid>[0-9a-z-]+)$', views.sim_started, name='sim_started'),
	url(r'^result/(?P<taskid>[0-9a-z-]+)$', views.result, name='result'),
]
