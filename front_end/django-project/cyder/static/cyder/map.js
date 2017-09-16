var mymap = L.map('map').setView([51.505, -0.09], 13);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(mymap);

var getJSON = function(url, callback) {
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

getJSON("/cyder/get_model/BU0001", function(err, json){
    if(err != null) { alert("Erreur: " + err); return; }
    model = json;
    
    for(line of model.lines)
        L.polygon([line.from, line.to], {
            color: 'blue'
        }).addTo(mymap);
    
    for(node of model.nodes)
        L.circle([node.latitude, node.longitude], {
            color: 'red',
            fillColor: '#f03',
            fillOpacity: 0.5,
            radius: 3
        }).addTo(mymap);
})
