function getJSON(url, callback) {
    var xhr = new XMLHttpRequest();
    xhr.open('GET', url, true);
    xhr.responseType = 'json';
    xhr.onload = function() {
        var status = xhr.status;
        if (status === 200) {
            callback(null, xhr.response);
        } else {
            callback(status, xhr.response);
        }
    };
    try {
        xhr.send();
    }
    catch(err) {
        callback("Can't send request", null);
    }
};

var leaflet_map;
var leaflet_toplayers = [];
var html = {};

window.onload = function () {

    // Init map
    leaflet_map = L.map('map').setView([37.8,-122.0], 9);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
    }).addTo(leaflet_map);

    // Get DOM element
    html.modelmenu = document.getElementById('modelmenu')

    // Set events
    html.modelmenu.addEventListener("change", modelmenu_onchange)

    // Trigger onpopstate to initialise the page in the asked context
    history.replaceState(state, "", window.location.href);
    window.onpopstate({state: state});
};



function change_state() {


}

window.onpopstate = function(e) {
    state = e.state;
    if(state.modelname == "")
        display_models_list();
    else
        display_model(state.modelname);
}

function modelmenu_onchange() {
    var href;
    if(state.modelname == "")
        href = "./" + html.modelmenu.value;
    else
        href = "./" + html.modelmenu.value;
    state.modelname = html.modelmenu.value;

    // Trigger onpopstate to update the page in the asked context
    history.pushState(state, "", href);
    window.onpopstate({state: state});
}

function display_models_list() {
    for(layer of leaflet_toplayers)
        layer.remove();
    leaflet_toplayers = [];

    getJSON("../api/models/geojson", function(err, json){
        if(err != null) { alert("Erreur: " + err); return; }

        var onEachFeature = function(feature, layer) {
            layer.bindPopup(feature.properties.modelname + "<br><a onclick='popups_onclick(\"" + feature.properties.modelname + "\")'>Open</a>");
        }

        var layerGeoJson = L.geoJson(json, {
            onEachFeature: onEachFeature
            }).addTo(leaflet_map);
        leaflet_toplayers.push(layerGeoJson);
        leaflet_map.fitBounds(layerGeoJson.getBounds());

        var newHtml = '<option value=""></option>';
        for(feature of json.features)
            newHtml += '<option value="' + feature.properties.modelname + '">' + feature.properties.modelname + '</option>';
        html.modelmenu.innerHTML = newHtml;
    });
}

function popups_onclick(modelname) {
    state.modelname = modelname;

    // Trigger onpopstate to update the page in the asked context
    history.pushState(state, "", "./" + modelname);
    window.onpopstate({state: state});
}

function display_model(modelname) {
    for(layer of leaflet_toplayers)
        layer.remove();
    leaflet_toplayers = [];

    getJSON("../api/models/" + modelname + "/geojson", function(err, json){
        if(err != null) { alert("Erreur: " + err); return; }

        var pointToLayer = function(feature, latlng) {
            return L.circle(latlng, {
                color: 'red',
                weight: 2,
                fillOpacity: 1,
                radius: 3
                });
        }

        var layerGeoJson = L.geoJson(json, {
            pointToLayer: pointToLayer,
            }).addTo(leaflet_map);
        leaflet_toplayers.push(layerGeoJson);
        leaflet_map.fitBounds(layerGeoJson.getBounds());

        html.modelmenu.value = modelname;
    });
}
