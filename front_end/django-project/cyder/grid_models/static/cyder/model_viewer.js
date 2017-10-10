function getJSON(url) {
    return new Promise(function(resolve, reject) {
        var xhr = new XMLHttpRequest();
        xhr.open('GET', url, true);
        xhr.responseType = 'json';
        xhr.onload = function() {
            if (xhr.status === 200) {
                resolve(xhr.response);
            } else {
                reject(xhr);
            }
        };
        xhr.send();
    });
}

var url = "/model_viewer";
var leaflet_map;
var html = {};

class AllModelView extends viewlib.View {
    constructor() {
        if(AllModelView._instance)
            return AllModelView._instance;

        super();
        AllModelView._instance = this;
    }

    _onbuild(done) {
        getJSON("/api/models/geojson")
        .then(geojson => {
            var onEachFeature = function(feature, layer) {
                layer.bindPopup(
                    feature.properties.modelname +
                    "<br><button class='btn btn-primary btn-sm' " +
                        "onclick='popups_onclick(\"" + feature.properties.modelname + "\")'" +
                    ">Open</button>"
                );
            }

            this.layerGeoJson = L.geoJson(geojson, {
                onEachFeature: onEachFeature
            });

            done();
        });
    }

    _onshow(done) {
        html.modelmenu.value = '';
        history.replaceState(null, null, "./");
        this.layerGeoJson.addTo(leaflet_map);
        leaflet_map.fitBounds(this.layerGeoJson.getBounds());
        done();
    }

    _onhide(done) {
        this.layerGeoJson.remove();
        done();
    }
}

class ModelView extends viewlib.View {
    constructor(modelname) {
        if(ModelView._instances && ModelView._instances[modelname])
            return ModelView._instances[modelname];

        super();
        this.modelname = modelname;
        this.nodeViewFrame = new viewlib.ViewFrame(this);
        if(!ModelView._instances)
            ModelView._instances = {};
        ModelView._instances[modelname] = this;
    }

    _onbuild(done) {
        getJSON(`/api/models/${this.modelname}/geojson`)
        .then(geojson => {
            var pointToLayer = (feature, latlng) => {
                var circle = L.circle(latlng, {
                    color: 'red',
                    weight: 2,
                    fillOpacity: 1,
                    radius: 3
                });
                circle._leaflet_id = feature.properties.id;
                circle.on('click', (e) => {
                    this.nodeViewFrame.changeView(new ModelView.NodeView(e.target._leaflet_id));
                });
                return circle;
            }

            this.layerGeoJson = L.geoJson(geojson, {
                pointToLayer: pointToLayer
            });

            done();
        });
    }

    _onshow(done) {
        html.modelmenu.value = this.modelname;
        history.replaceState(null, null, `./${this.modelname}`);
        this.layerGeoJson.addTo(leaflet_map);
        leaflet_map.fitBounds(this.layerGeoJson.getBounds());
        done();
    }

    _onhide(done) {
        this.layerGeoJson.remove();
        done();
    }
}

ModelView.NodeView = class NodeView extends viewlib.View {
    constructor(node_id) {
        if(NodeView._instances && NodeView._instances[node_id])
            return NodeView._instances[node_id];

        super();
        this.node_id = node_id;
        if(!NodeView._instances)
            NodeView._instances = {};
        NodeView._instances[node_id] = this;
    }

    _onbuild(done) {
        this.nodeLayer = this.parentView.layerGeoJson.getLayer(this.node_id);
        getJSON(`/api/models/${this.parentView.modelname}/nodes/${this.node_id}`)
        .then(node => {
            var display = (num) => (num == null) ? "NA" : num;
            this.nodeLayer.bindPopup(
                `Node ${this.node_id}
                <br>VoltageA: ${display(node.VA)}
                <br>VoltageB: ${display(node.VB)}
                <br>VoltageC: ${display(node.VC)}`
            );
            done();
        });
    }

    _onshow(done) {
        this.nodeLayer.openPopup();
        done();
    }

    _onhide(done) {
        this.nodeLayer.closePopup();
        done();
    }
}

var mainViewFrame = new viewlib.ViewFrame();

window.onload = function () {
    leaflet_map = L.map('map').setView([37.8,-122.0], 9);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
    }).addTo(leaflet_map);

    html.modelmenu = document.getElementById('modelmenu');

    html.modelmenu.addEventListener("change", modelmenu_onchange);

    getJSON("../api/models").then((models) => {
        var newHtml = '<option value="">All</option>';
        for(var model of models)
            newHtml += `<option value="${model.name}">${model.name}</option>`;
        html.modelmenu.innerHTML = newHtml;

        if(djangoContext.modelname == '') {
            return mainViewFrame.changeView(new AllModelView());
        } else {
            return mainViewFrame.changeView(new ModelView(djangoContext.modelname));
        }
    });
};

function modelmenu_onchange() {
    if(html.modelmenu.value == '')
        mainViewFrame.changeView(new AllModelView());
    else
        mainViewFrame.changeView(new ModelView(html.modelmenu.value));
}

function popups_onclick(modelname) {
    mainViewFrame.changeView(new ModelView(modelname));
}
