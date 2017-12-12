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
    let devices = CyderAPI.Device.getAll(modelName);
    let pvs = CyderAPI.PV.getAll(modelName);
    devices = await devices;
    pvs = await pvs;
    let layer = L.layerGroup([]);
    for(let pv of pvs.values()) {
        let device = devices.get(pv.device);
        let marker = L.circleMarker([device.latitude, device.longitude]);
        onEach(pv, device, marker);
        layer.addLayer(marker);
    }
    return layer;
}

export async function createLoadLayer(modelName, onEach = ()=>{}) {
    let devices = CyderAPI.Device.getAll(modelName);
    let loads = CyderAPI.Load.getAll(modelName);
    devices = await devices;
    loads = await loads;
    let layer = L.layerGroup([]);
    for(let load of loads.values()) {
        let device = devices.get(load.device);
        let marker = L.circleMarker([device.latitude, device.longitude]);
        onEach(load, device, marker);
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
        let device = devices.get(load.device);
        let loadValue = 0;
        for(let phase of phases)
            loadValue += load['SpotKW'+phase]===null ? 0 : load['SpotKW'+phase];
        if(loadValue > maxLoad) maxLoad = loadValue;
        return [device.latitude, device.longitude , loadValue];
    })

    let heatLayer = L.heatLayer(data, {max: maxLoad, maxZoom: 1, radius: 10, blur:5});
    return heatLayer;
}
