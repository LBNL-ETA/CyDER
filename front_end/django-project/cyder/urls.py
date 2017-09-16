from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^map$', views.map, name='map'),
    url(r'^get_model/(?P<modelname>[0-9a-zA-Z]+)$', views.get_model, name='get_model'),
    url(r'^ask_model$', views.ask_model, name='ask_model'),
    url(r'^updade_db/(?P<taskid>[0-9a-z-]+)$', views.update_db, name='update_db'),
    url(r'^db_updated$', views.db_updated, name='db_updated'),
]
