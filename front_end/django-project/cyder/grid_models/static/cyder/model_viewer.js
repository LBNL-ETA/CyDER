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
    if(state.modelfile == "")
        display_models_list();
    else
        display_model(state.modelfile);
}

function modelmenu_onchange() {
    var href;
    if(state.modelfile == "")
        href = "./" + html.modelmenu.value;
    else
        href = "./" + html.modelmenu.value;
    state.modelfile = html.modelmenu.value;

    // Trigger onpopstate to update the page in the asked context
    history.pushState(state, "", href);
    window.onpopstate({state: state});
}

function display_models_list() {
    for(layer of leaflet_toplayers)
        layer.remove();
    leaflet_toplayers = [];

    getJSON("../api/geojson/models", function(err, json){
        if(err != null) { alert("Erreur: " + err); return; }

        var onEachFeature = function(feature, layer) {
            layer.bindPopup(feature.properties.modelfile + "<br><a onclick='popups_onclick(\"" + feature.properties.modelfile + "\")'>Open</a>");
        }

        var layerGeoJson = L.geoJson(json, {
            onEachFeature: onEachFeature
            }).addTo(leaflet_map);
        leaflet_toplayers.push(layerGeoJson);
        leaflet_map.fitBounds(layerGeoJson.getBounds());

        var newHtml = '<option value=""></option>';
        for(feature of json.features)
            newHtml += '<option value="' + feature.properties.modelfile + '">' + feature.properties.modelfile + '</option>';
        html.modelmenu.innerHTML = newHtml;
    });
}

function popups_onclick(modelfile) {
    state.modelfile = modelfile;

    // Trigger onpopstate to update the page in the asked context
    history.pushState(state, "", "./" + modelfile);
    window.onpopstate({state: state});
}

function display_model(modelfile) {
    for(layer of leaflet_toplayers)
        layer.remove();
    leaflet_toplayers = [];

    getJSON("../api/geojson/models/" + modelfile, function(err, json){
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

        html.modelmenu.value = modelfile;
    });
}
