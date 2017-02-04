import coreapi
from rest_framework.filters import BaseFilterBackend


class NodeResultFilter(BaseFilterBackend):
  def get_schema_fields(self, view):
    fields = [
      coreapi.Field(name="simulation_id", description="simulation id", required=True, location='query'),
      coreapi.Field(name="node_id", description="node id", required=False, location='query'),
    ]
    return fields


class CalibrationHistoryFilter(BaseFilterBackend):
  def get_schema_fields(self, view):
    fields = [
      coreapi.Field(name="model_id", description="model id", required=True, location='query'),
    ]
    return fields
