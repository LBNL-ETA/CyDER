from django.conf.urls import url, include

urlpatterns = [
    url(r'^model_viewer/', include('cyder.models.urls')),
    url(r'^projects/', include('cyder.projects.urls')),
    url(r'^api/', include('cyder.api.urls', namespace='api')),
    url(r'^', include('cyder.main.urls')),
]
