from rest_framework import serializers
from cyder.grid_models.models import Model

class ModelSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Model
        fields = '__all__'
        extra_kwargs = { 'url': { 'view_name': 'api:model-detail', 'lookup_field': 'name'}}
