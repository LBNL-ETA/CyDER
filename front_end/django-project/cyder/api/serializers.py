from rest_framework import serializers
from cyder.grid_models.models import Model

class ModelSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Model
        fields = '__all__'
