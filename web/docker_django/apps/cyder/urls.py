from django.conf.urls import url, include
from . import views
from . import api
from rest_framework import routers
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='CyDER API')

router = routers.DefaultRouter()
router.register(r'model', views.ModelViewSet)
router.register(r'simulation', views.UserModelViewSet)
router.register(r'simulation_node_result', views.NodeResultViewSet)
router.register(r'calibration', views.CalibrationViewSet)
router.register(r'ev_scenario', views.ElectricVehicleScenarioViewSet)

urlpatterns = [
    url(r'^api2/', include(router.urls)),
    url(r'^api2/upmu/(?P<date_from>[^/]+)/(?P<date_to>[^/]+)/(?P<location>[^/]+)/$', views.upmu, name='upmu'),
    url(r'^documentation/$', schema_view),

    # Normal view to navigate in the website
    url(r'^home/$', views.home, name='home'),
    url(r'^model/(?P<id>\d+)/$', views.model, name='model'),
    url(r'^my_models/', views.my_models, name='my_models'),
    url(r'^calibration/(?P<id>\d+)/$', views.calibration, name='calibration'),
    url(r'^my_models_general_settings/(?P<id>\d+)/$', views.my_models_general_settings, name='my_models_general_settings'),
    url(r'^my_models_add_devices/(?P<id>\d+)/$', views.my_models_add_devices, name='my_models_add_devices'),
    url(r'^my_models_settings/(?P<id>\d+)/$', views.my_models_settings, name='my_models_settings'),
    url(r'^my_models_review/(?P<id>\d+)/$', views.my_models_review, name='my_models_review'),
    url(r'^show_upmu_data/$', views.show_upmu_data, name='show_upmu_data'),
    url(r'^show_node_result/(?P<id>\d+)/$', views.show_node_result, name='show_node_result'),

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
    url(r'^api/upmu/get/$', api.get_upmu_data, name='get-upmu-data'),
]
