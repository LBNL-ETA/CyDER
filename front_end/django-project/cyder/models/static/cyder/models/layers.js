import CyderAPI from '../api.js';

/* componenet Layer
Base component for a layer. It should be heritated using Vuejs compnents mixin to create component.
To work, a layer component using this Layer mixin must at least implement a getLayer() method wich must return the Leaflet layer object (or the Promise of such layer).
keepOrder: if set, the map will ensure to add this layer after the previous one, so it's drawn on top of it.
Otherwise all layers are added as soon as their Promise resolves.
*/
export const Layer = {
    props: {
        fit: Boolean,
        keepOrder: Boolean,
    },
    data() { return {
        map: null,
    };},
    mounted() {
        if(this.$parent.getLeafletMap instanceof Function)
            this.map = this.$parent.getLeafletMap();
    },
    destroyed() {
        if(this.map !== null)
            this.map.removeLayer(this);
    },
    methods: {
        redraw() {
            // Redraw the layer by forcing a call to the map watcher
            // This induces a call to getLayer()
            let map = this.map;
            this.map = null;
            this.map = map;
        }
    },
    watch: {
        fit: {
            immediate: true,
            handler(val) {
                if(this.map !== null)
                    this.$parent.fitBounds(this);
            },
        },
        map: {
            handler(newMap, oldMap) {
                if(oldMap !== null)
                    oldMap.removeLayer(this);
                if(newMap !== null) {
                    newMap.addLayer(this.getLayer(), this, this.keepOrder);
                    if(this.fit)
                        newMap.fitBounds(this);
                }
            },
        },
    },
    template: '<div></div>',
}

export async function createAllModelsLayer(onEachFeature = ()=>{}) {
    let geojson = await CyderAPI.rest('GET', '/api/models/geojson/');
    return L.geoJson(geojson, {
        onEachFeature
    });
}

export const OpenModelLayer = {
    mixins: [Layer],
    data() { return {
        selectedModel: '',
    };},
    methods: {
        getLayer() {
            let addPopup = (feature, layer) => {
                layer.bindPopup(this.$refs.popup);
                layer.on('click', () => { this.selectedModel = feature.properties.modelname; });
            };
            return createAllModelsLayer(addPopup);
        },
    },
    template: `<div style="display: none;">
        <div ref="popup">
            {{ selectedModel }}<br>
            <button class='btn btn-primary btn-sm' @click="$emit('open', {modelName: selectedModel})">Open</button>
        </div>
    </div>`,
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

export const ModelLayer = {
    mixins: [Layer],
    props: {
        modelName: null,
    },
    methods: {
        getLayer() {
            return createModelLayer(this.modelName);
        },
    },
    watch: {
        modelName(val) {
            this.redraw();
        }
    },
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

export async function createLoadHeatmapLayer(modelName, phases) {
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

export const LoadHeatmapLayer = {
    mixins: [Layer],
    props: {
        modelName: String,
        phases: null,
        setMaxScale: null,
    },
    methods: {
        getLayer() {
            this.$data._layer = createLoadHeatmapLayer(this.modelName, this.phases);
            this.$data._layer.then(layer => {
                this.$data._layer = layer;
                this.$emit('maxScaleChange', layer.options.max);
            });
            return this.$data._layer;
        },
    },
    watch: {
        phases() {
            if(this.map === null)
                return;
            this.map.removeLayer(this);
            this.map.addLayer(this.getLayer(), this);
        },
        setMaxScale(val) {
            if(this.$data._layer !== undefined && !(this.$data._layer instanceof Promise)) {
                this.$data._layer.setOptions({max: val});
                this.$emit('maxScaleChange', val);
            }
        },
        modelName(val) {
            // Redraw the layer by forcing a call to the map watcher
            let map = this.map;
            this.map = null;
            this.map = map;
        },
    }
}
