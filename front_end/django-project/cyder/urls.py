from django.urls import path, include

urlpatterns = [
    path('model_viewer/', include('cyder.models.urls')),
    path('projects/', include('cyder.projects.urls')),
    path('api/', include('cyder.api.urls', namespace='api')),
    path('', include('cyder.main.urls')),
]
