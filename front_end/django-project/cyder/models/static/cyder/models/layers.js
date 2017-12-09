import CyderAPI from '../api.js';

export async function createAllModelsLayer(onEachFeature = ()=>{}) {
    let geojson = await CyderAPI.rest('GET', '/api/models/geojson/');
    return L.geoJson(geojson, {
        onEachFeature
    });
}

export async function createModelLayer(modelName, onEachFeature = ()=>{}) {
    let geojson = await CyderAPI.rest('GET', `/api/models/${encodeURI(modelName)}/geojson/`);
    let pointToLayer = (feature, latlng) => {
        var circle = L.circle(latlng, {
            color: 'red',
            weight: 2,
            fillOpacity: 1,
            radius: 3
        });
        return circle;
    }
    return L.geoJson(geojson, {
        pointToLayer,
        onEachFeature
    });
}

export async function createPVLayer(modelName, onEach = ()=>{}) {
    let pvs = Array.from((await CyderAPI.Device.getAll(modelName)).values())
        .filter((device) => device.device_type == 39);
    let layer = L.layerGroup([]);
    for(let pv of pvs) {
        let marker = L.circleMarker([pv.latitude, pv.longitude]);
        onEach(pv, marker);
        layer.addLayer(marker);
    }
    return layer;
}

export async function createLoadLayer(modelName, onEach = ()=>{}) {
    let loads = Array.from((await CyderAPI.Device.getAll(modelName)).values())
        .filter((device) => device.device_type == 14);
    let layer = L.layerGroup([]);
    for(let load of loads) {
        let marker = L.circleMarker([load.latitude, load.longitude]);
        onEach(load, marker);
        layer.addLayer(marker);
    }
    return layer;
}

export async function createLoadHeatLayer(modelName, phases) {
    let devices = CyderAPI.Device.getAll(modelName);
    let loads = CyderAPI.Load.getAll(modelName);
    devices = await devices;
    loads = await loads;

    let maxLoad = 0;
    let data = Array.from(loads.values()).map((load) => {
        let device = devices.get(load.device_number);
        let loadValue = 0;
        for(let phase of phases)
            loadValue += load['SpotKW'+phase]===null ? 0 : load['SpotKW'+phase];
        if(loadValue > maxLoad) maxLoad = loadValue;
        return [device.latitude, device.longitude , loadValue];
    })

    let heatLayer = L.heatLayer(data, {max: maxLoad, maxZoom: 1, radius: 10, blur:5});
    return heatLayer;
}
