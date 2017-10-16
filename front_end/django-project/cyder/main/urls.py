from django.conf.urls import url
from . import views

from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^login/$', auth_views.login, {'template_name': 'cyder/login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),
    url(r'^$', views.home, name='home'),
]
