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

class View {
    constructor(viewSet) {
        if(this.constructor.name == "View") throw "View is an abstract class";
        this._viewSet = viewSet;
        this._isbuilt = false;
    }

    build() {
        return new Promise(this._onbuild)
        .then(() => { this._isbuilt = true;});
    }
    show() {
        return Promise.resolve((() => {
            if(!this._isbuilt)
                return this.build();
        })()).then(() => {
            return new Promise(this._onshow);
        });
    }
    hide() {
        return new Promise(this._onhide);
    }
}

class GenericView extends View {
    constructor(viewSet, func) {
        super(viewSet);
        this._onbuild = func.onbuild;
        this._onshow = func.onshow;
        this._onhide = func.onhide;
    }
}

class ViewSet {
    constructor() {
        this._currentView = null;
        this._isshown = true;
    }
    get currentView() { return this._currentView; }

    changeView(view) {
        return Promise.resolve((() => {
            if(this._isshown)
                return this._currentView.hide();
        })()).then(() => {
            this._currentView = view;
            if(this._isshown)
                return this._currentView.show();
        });
    }
    show() {
        this._isshown = true;
        if(this._currentView)
            return this._currentView.show();
        else
            return Promise.resolve();
    }
    hide() {
        this._isshown = false;
        if(this._currentView)
            return this._currentView.hide();
        else
            return Promise.resolve();
    }
}





var mainViewSet = new ViewSet();
var allModelView = new GenericView(mainViewSet, {
    onbuild: function(done) {
        setTimeout(() => {console.log('built!'); done();}, 1000);
    },
    onshow: function(done) {
        setTimeout(() => {console.log('shown!'); done();}, 1000);
    },
    onhide: function(done) {
        setTimeout(() => {console.log('hide!'); done();}, 1000);
    }
});
var other = new GenericView(mainViewSet, {
    onbuild: function(done) {
        setTimeout(() => {console.log('built!'); done();}, 1000);
    },
    onshow: function(done) {
        setTimeout(() => {console.log('shown!'); done();}, 1000);
    },
    onhide: function(done) {
        setTimeout(() => {console.log('hide!'); done();}, 1000);
    }
});

console.log("start");
mainViewSet.hide().then(() => {
    return mainViewSet.changeView(other);
}).then(() => {
    return mainViewSet.show();
    // built!
    // shown!
}).then(() => {
    return mainViewSet.changeView(allModelView);
    // hide!
    // built!
    // shown!
}).then(() => {
    return mainViewSet.hide();
    // hide!
}).then(() => {
    return mainViewSet.show();
    // shown!
}).then(() => {
    console.log("end");
});




/*
class AllModelState extends statelib.GenericState {
    constructor() {
        super();
    }

    _onrestore() {
        console.log("Restore AllModelState");
        html.modelmenu.value = "";

        getJSON("../api/models/geojson").then((json) => {
            var onEachFeature = function(feature, layer) {
                layer.bindPopup(feature.properties.modelname + "<br><button class='btn btn-primary btn-sm' onclick='popups_onclick(\"" + feature.properties.modelname + "\")'>Open</button>");
            }

            this.data.layerGeoJson = L.geoJson(json, {
                onEachFeature: onEachFeature
                }).addTo(leaflet_map);
            leaflet_map.fitBounds(this.data.layerGeoJson.getBounds());
        })
        .catch((err) => {
            if(err.constructor.name == "XMLHttpRequest")
                alert("Error: " + errxhr.status);
            else
                throw err;
        });
    }
    _onabolish() {
        console.log("Abolish AllModelState");
        this.data.layerGeoJson.remove();
    }
}
statelib.registerStateClass(AllModelState);

class ModelState extends statelib.GenericState {
    constructor(modelname) {
        super();

        this.modelname = modelname;
    }

    _onrestore() {
        console.log("Restore ModelState:" + this.modelname);
        html.modelmenu.value = this.modelname;

        getJSON("../api/models/" + this.modelname + "/geojson").then((json) => {
            var pointToLayer = (feature, latlng) => {
                var circle = L.circle(latlng, {color: 'red', weight: 2, fillOpacity: 1, radius: 3});
                circle._leaflet_id = feature.properties.id;
                circle.on('click', (e) => {
                    (new NodeInfoState(e.target._leaflet_id)).restore();
                });
                return circle;
            }

            this.data.layerGeoJson = L.geoJson(json, {
                pointToLayer: pointToLayer,
                }).addTo(leaflet_map);
            leaflet_map.fitBounds(this.data.layerGeoJson.getBounds());
        })
        .catch((err) => {
            if(err.constructor.name == "XMLHttpRequest")
                alert("Error: " + errxhr.status);
            else
                throw err;
        });
    }
    _onabolish() {
        console.log("Abolish ModelState:" + this.modelname);
        this.data.layerGeoJson.remove();
    }
}
statelib.registerStateClass(ModelState);

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
            (new AllModelState()).restore();
        } else {
            (new ModelState(djangoContext.modelname)).restore();
        }

        statelib.replaceState(window.location.href);
    })
    .catch((err) => {
        if(err.constructor.name == "XMLHttpRequest")
            alert("Error: " + errxhr.status);
        else
            throw err;
    });
};

function modelmenu_onchange() {
    if(html.modelmenu.value == '') {
        (new AllModelState()).restore();
    } else {
        (new ModelState(html.modelmenu.value)).restore();
    }

    statelib.pushState("./" + html.modelmenu.value);
}

function popups_onclick(modelname) {
    (new ModelState(modelname)).restore();
    statelib.pushState("./" + modelname);
}
*/
