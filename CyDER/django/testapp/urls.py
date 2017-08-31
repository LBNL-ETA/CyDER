from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^start_sim$', views.start_sim, name='start_sim'),
	url(r'^sim_started$', views.sim_started, name='sim_started'),
	url(r'^result$', views.result, name='result'),
]
