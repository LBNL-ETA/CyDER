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
    xhr.send();
};

class Model {
    constructor() {
        this.objects = []
    }
    load(json) {
        for(var line of json.lines)
            this.objects.push(L.polyline([line.from, line.to], {
                color: 'blue'
            }));
        
        for(var node of json.nodes)
            this.objects.push(L.circle([node.latitude, node.longitude], {
                color: 'red',
                fillColor: '#f03',
                fillOpacity: 0.5,
                radius: 3
            }));
    }
    addToMap(map) {
        for(var object of this.objects)
            object.addTo(map);
    }
    remove() {
        for(var object of this.objects)
            object.remove();
    }
}

var leaflet_map;
var model;
var html = {}

function init_map() {
    leaflet_map = L.map('map').setView([37.8,-122.0], 9);
    
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
    }).addTo(leaflet_map);
}

window.onload = function () {
    init_map();
    html.modelmenu = document.getElementById('modelmenu')
    html.modelmenu.addEventListener("change", modelmenu_change)
    
    modelmenu_change();
};

function modelmenu_change() {
    if(model)
        model.remove();
    
    model = new Model();
    getJSON("./get_model/" + html.modelmenu.value, function(err, json){
        if(err != null) { alert("Erreur: " + err); return; }
        model.load(json);
        model.addToMap(leaflet_map);
    });
}
