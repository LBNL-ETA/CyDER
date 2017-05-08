from django.conf.urls import url, include
from . import views
from . import api
from rest_framework import routers
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='CyDER API')

router = routers.DefaultRouter()
router.register(r'model', api.ModelViewSet)
router.register(r'project', api.ProjectViewSet)
router.register(r'project_model', api.ProjectModelViewSet)
router.register(r'project_model_node_result', api.NodeResultViewSet)
router.register(r'calibration', api.CalibrationViewSet)
router.register(r'project_model_ev_scenario', api.ElectricVehicleScenarioViewSet)
router.register(r'node', api.NodeViewSet)

urlpatterns = [
    url(r'^api/', include(router.urls)),
    url(r'^api/upmu/(?P<date_from>[^/]+)/(?P<date_to>[^/]+)/(?P<location>[^/]+)/$', api.upmu, name='upmu'),
    url(r'^docs/$', schema_view),

    # Normal view to navigate in the website
    url(r'^home/$', views.home, name='home'),
    url(r'^model/(?P<id>\d+)/$', views.model, name='model'),
    url(r'^create_project/', views.create_project, name='create_project'),
    url(r'^add_model/(?P<id>\d+)/$', views.add_model, name='add_model'),
    url(r'^my_projects/$', views.my_projects, name='my_projects'),
    url(r'^my_project_settings/(?P<id>\d+)/$', views.my_project_settings, name='my_project_settings'),
    url(r'^my_project_model_add_devices/(?P<id>\d+)/$', views.my_model_add_devices, name='my_model_add_devices'),
    url(r'^my_project_model_settings/(?P<id>\d+)/$', views.my_model_settings, name='my_model_settings'),
    url(r'^my_project_model_scenarios/(?P<id>\d+)/$', views.my_model_scenarios, name='my_model_scenarios'),
    url(r'^my_project_review/(?P<id>\d+)/$', views.my_project_review, name='my_project_review'),
    url(r'^calibration/(?P<id>\d+)/$', views.calibration, name='calibration'),
    url(r'^show_upmu_data/$', views.show_upmu_data, name='show_upmu_data'),
    url(r'^my_project_node_result/(?P<id>\d+)/$', views.my_project_node_result, name='my_project_node_result'),
]
