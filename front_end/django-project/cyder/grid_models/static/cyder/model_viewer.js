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

var mainViewSet = new viewlib.ViewSet();

class AllModelView extends viewlib.View {
    constructor() {
        if(AllModelView._instance) return AllModelView._instance;
        super(mainViewSet);
        AllModelView._instance = this;
    }

    _onbuild(done) {
        getJSON("/api/models/geojson").then(geojson => {
            this.geojson = geojson;
            done();
        });
    }

    _onshow(done) {
        var onEachFeature = function(feature, layer) {
            layer.bindPopup(feature.properties.modelname + "<br><button class='btn btn-primary btn-sm' onclick='popups_onclick(\"" + feature.properties.modelname + "\")'>Open</button>");
        }

        this.layerGeoJson = L.geoJson(this.geojson, {
            onEachFeature: onEachFeature
            }).addTo(leaflet_map);
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
        if(ModelView._instances && ModelView._instances[modelname]) return ModelView._instances[modelname];
        super(mainViewSet);
        this.modelname = modelname;
        if(!ModelView._instances)
            ModelView._instances = {};
        ModelView._instances[modelname] = this;
    }

    _onbuild(done) {
        getJSON("/api/models/" + this.modelname + "/geojson").then(geojson => {
            this.geojson = geojson;
            done();
        })
    }

    _onshow(done) {
        html.modelmenu.value = this.modelname;

        var pointToLayer = (feature, latlng) => {
            var circle = L.circle(latlng, {color: 'red', weight: 2, fillOpacity: 1, radius: 3});
            circle._leaflet_id = feature.properties.id;
            circle.on('click', (e) => {
                //(new NodeInfoState(e.target._leaflet_id)).restore();
            });
            return circle;
        }

        this.layerGeoJson = L.geoJson(this.geojson, {
            pointToLayer: pointToLayer,
            }).addTo(leaflet_map);
        leaflet_map.fitBounds(this.layerGeoJson.getBounds());

        done();
    }

    _onhide(done) {
        this.layerGeoJson.remove();
        done();
    }
}

mainViewSet.changeView(new AllModelView());

/*
class NodeInfoState extends statelib.GenericState {
    constructor(node_id, parent = statelib.currentstate()) {
        if(!(parent instanceof ModelState)) throw "NodeInfoState can't be created is this context"
        super(parent, '.select');

        this.node_id = node_id;
    }

    _onrestore() {
        console.log("Restore NodeInfoState:"+this.node_id);
        var nodeLayer = this.parent.data.layerGeoJson.getLayer(this.node_id);
        getJSON("../api/models/"+this.parent.modelname+"/nodes/"+this.node_id).then((node) => {
            nodeLayer.bindPopup("Node "+this.node_id+"<br>VoltageA: "+node.VA+"<br>VoltageB: "+node.VB+"<br>VoltageC: "+node.VC);
            nodeLayer.openPopup();
        })
        .catch((err) => {
            if(err.constructor.name == "XMLHttpRequest")
                alert("Error: " + errxhr.status);
            else
                throw err;
        });
    }
    _onabolish() {
        console.log("Abolish NodeInfoState:"+this.node_id);
    }
}
statelib.registerStateClass(NodeInfoState);

window.onpopstate = statelib.onpopstate;
*/
window.onload = function () {
    // Init map
    leaflet_map = L.map('map').setView([37.8,-122.0], 9);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
    }).addTo(leaflet_map);

    // Get DOM element
    html.modelmenu = document.getElementById('modelmenu');

    // Set events
    html.modelmenu.addEventListener("change", modelmenu_onchange);

    getJSON("../api/models").then(function(models) {
        var newHtml = '<option value="">All</option>';
        for(var model of models)
            newHtml += '<option value="' + model.name + '">' + model.name + '</option>';
        html.modelmenu.innerHTML = newHtml;
    })
    .then(() => {
        if(djangoContext.modelname == '') {
            mainViewSet.changeView(new AllModelView());
        } else {
            mainViewSet.changeView(new ModelView(djangoContext.modelname));
        }

        //statelib.replaceState(window.location.href);
    });
};

function modelmenu_onchange() {
    if(html.modelmenu.value == '') {
        mainViewSet.changeView(new AllModelView());
    } else {
        mainViewSet.changeView(new ModelView(html.modelmenu.value));
    }

    //statelib.pushState("./" + html.modelmenu.value);
}

function popups_onclick(modelname) {
    mainViewSet.changeView(new ModelView(modelname));
    //statelib.pushState("./" + modelname);
}
