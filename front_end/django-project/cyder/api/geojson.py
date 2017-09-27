from django.http import HttpResponse
from django.db.models import Q
from cyder.grid_models.models import Model, Node, Section, Device
import json

def models_list(request):
    models = Model.objects.all()
    
    features = []
    for model in models:
        first_node = Node.objects.filter(model=model)[0]
        features.append({
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [first_node.longitude,first_node.latitude]
                },
            "properties": { "modelfile": model.filename }
            });
    geojson = json.dumps({"type": "FeatureCollection", "features": features }, separators=(',',':'))

    return HttpResponse(geojson)

def get_model(request, modelfile):
    model = Model.objects.get(filename=modelfile)
    nodes = Node.objects.filter(model=model)
    lines = Device.objects.filter(Q(model=model), Q(device_type=10) | Q(device_type=13)).select_related('section__from_node', 'section__to_node')

    features = []
    for line in lines:
        features.append({
            "type": "Feature",
            "geometry": {
                "type": "LineString",
                "coordinates": [
                    [line.section.from_node.longitude,line.section.from_node.latitude],
                    [line.section.to_node.longitude,line.section.to_node.latitude]
                    ]
                },
            });
    for node in nodes:
        features.append({
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [node.longitude,node.latitude]
                },
            });
    geojson = json.dumps({"type": "FeatureCollection", "features": features }, separators=(',',':'))

    return HttpResponse(geojson)
