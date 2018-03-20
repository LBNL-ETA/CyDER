'use strict';
import CyderAPI from '../api.js';
import { ModelLayer, LoadHeatmapLayer } from './layers.js';
import notifyRESTError from '../api-notify-error.js';

export const ModelSelector = {
    model: { prop: 'value', event: 'change' },
    props: {
        allowEmpty: Boolean,
        value: String,
        initModels: {
            default() { return (async () => {
                return Array.from((await CyderAPI.Model.getAll()).keys());
            })(); }
        },
    },
    data() { return {
        models: this.initModels,
    };},
    template: `
        <select @change="$emit('change', $event.target.value)" :value="value" class="custom-select" style="width: 100%":disabled="isLoading">
            <option v-if="allowEmpty" value=""></option>
            <option v-if="!isLoading" v-for="model in models">{{ model }}</option>
        </select>`,
    computed: {
        isLoading() { return this.models instanceof Promise; },
    },
    watch: {
        models: {
            immediate: true,
            handler(value) {
                if(value instanceof Promise)
                    value.then((models) => { this.models = models; });
            },
        }
    },
    updated() { this.$el.value = this.value; }
};

import {Spinner} from './spin.js';
export const LeafletMap = {
    data() { return {

    };},
    created() {
        this.$data._map = null;
        let m = new Map();
        this.$data._layers = m;
        this.$emit('getmapinstance', m);
        this.$data._loadingLayers = 0;
        this.$data._lastLayerId = null;
        this.$data._loadingSpinner = new Spinner();
    },
    mounted() {
        this.$data._map = L.map(this.$el, {preferCanvas: true}).setView([37.8,-122.0], 9);
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            maxZoom: 19,
            attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
        }).addTo(this.$data._map);
        for(let layer of this.$data._layers.values()) {
            if(!(layer instanceof Promise))
                layer.addTo(this.$data._map);
        }
        this._updateLoadingLayers(0);
    },
    template: `<div><slot></slot></div>`,

    methods: {
        getLeafletMap() { return this; },
        _updateLoadingLayers(val) {
            this.$data._loadingLayers += val;
            if(this.$data._loadingLayers > 0) {
                if(this._isMounted) this.$data._loadingSpinner.spin(this.$el);
            }
            else
                this.$data._loadingSpinner.stop();
        },
        addLayer(layer, id, keepOrder = false) {
            if(this.$data._layers.has(id))
                throw new Error("A layer with this id already ");

            let isAddedProm = (async () => {
                this._updateLoadingLayers(+1);
                if(keepOrder && this.$data._lastLayerId !== null)
                    await this.$data._layers.get(this.$data._lastLayerId);
                layer = await layer;
                if(isAddedProm !== undefined && this.$data._layers.get(id) !== isAddedProm)
                    return false; // The layer have been removed while loading
                if(this._isMounted) layer.addTo(this.$data._map);
                this.$data._layers.set(id, layer);
                this._updateLoadingLayers(-1);
                return true;
            })();
            this.$data.Id = id;
            if(this.$data._layers.has(id))
                return true;
            this.$data._layers.set(id, isAddedProm);
            this.$data._lastLayerId = id;
            return isAddedProm;
        },
        removeLayer(id) {
            let layer = this.$data._layers.get(id);
            if(!layer)
                return false;
            this.$data._layers.delete(id);
            if(this.$data.Id === id) {
                this.$data._lastLayerId = null;
                for(let id of this.$data._layers.keys()) this.$data._lastLayerId = id;
            }
            if(layer instanceof Promise)
                this._updateLoadingLayers(-1);
            else
                layer.remove();
            return true;
        },
        removeLayers() { // deprecated
            for(let layerId of this.$data._layers.keys())
                this.removeLayer(layerId);
        },
        async fitBounds(id) {
            let layer = this.$data._layers.get(id);
            if(layer instanceof Promise) {
                let isAddedProm = layer;
                if((await isAddedProm) === false)
                    return false; // The layer have been removed while loading
                layer = this.$data._layers.get(id);
            }
            this.$data._map.fitBounds(layer.getBounds());
            return true;
        },
    },
    computed: {
        map() { return this.$data._map; },
    },
};

export const RemoteLeafletMap = {
    props: {
        map: {required: true},
    },
    template: `<div><slot></slot></div>`,
    methods: {
        getLeafletMap() { return this.map; }
    },
    watch: {
        map(val) {
            for(let child of this.$children)
                child.map = val;
        },
    }
};

export const LoadHeatmapControl = {
    props: {
        map: null,
        modelName: String,
    },
    data() { return {
        phases: [],
        maxScale: null,
    };},
    components: { RemoteLeafletMap, LoadHeatmapLayer },
    template: `<div>
        <remote-leaflet-map :map="map">
            <load-heatmap-layer v-if="phases.length != 0" :model-name="modelName" :phases="phases" :set-max-scale="maxScale" @maxScaleChange="maxScale=$event"></load-heatmap-layer>
        </remote-leaflet-map>
        <div class="btn-group btn-group-sm" role="group" style="display: flex; margin-bottom: 1em;">
            <button type="button" class="btn btn-secondary" :class="{disabled:phases.indexOf('A')>=0}" @click="tooglePhase('A')" style="width: 33.3%;">Phase A</button>
            <button type="button" class="btn btn-secondary" :class="{disabled:phases.indexOf('B')>=0}" @click="tooglePhase('B')" style="width: 33.3%;">Phase B</button>
            <button type="button" class="btn btn-secondary" :class="{disabled:phases.indexOf('C')>=0}" @click="tooglePhase('C')" style="width: 33.3%;">Phase C</button>
        </div>
        <div v-if="phases.length != 0" style="display: table;">
            <div>0 </div>
            <div style="display: table-cell; width: 100%; height: 1em; background: linear-gradient(to right, rgba(0,0,255,0.1), rgba(0,0,255,0.5), lime, yellow, red);"></div>
            <input style="display: table-cell; width:65px" type="number" v-model="maxScale">
        </div>
    </div>`,
    methods: {
        tooglePhase(phase) {
            let i = this.phases.indexOf(phase);
            if(i >= 0)
                this.phases.splice(i,1);
            else
                this.phases.push(phase);
        },
    },
};

export const ModelViewer = {
    props: {
        modelName: String,
        map: null,
    },
    data() { return {
        model: null,
    };},
    components: { RemoteLeafletMap, ModelLayer, LoadHeatmapControl },
    template: `<div>
        <remote-leaflet-map :map="map">
            <model-layer :model-name="modelName" fit></model-layer>
        </remote-leaflet-map>
        <div v-if="model !== null" class="row" style="margin-bottom: 1rem">
            <div class=col-lg-4>
                <div class="card">
                    <div class="card-header">
                        Infos
                    </div>
                    <div class="card-body">
                        Model name: {{ this.model.name }}<br>
                        Nodes count: <span id="nodescount"></span><br>
                        Devices count: <span id="devicescount"></span><br>
                    </div>
                </div>
            </div>
            <div class="col-lg-4">
                <div class="card">
                    <div class="card-header">
                        Loads (kW)
                    </div>
                    <div id="" class="card-body">
                        <load-heatmap-control :model-name="modelName" :map="map"></load-heatmap-control>
                    </div>
                </div>
            </div>
            <div class="col-lg-4">
                <div class="card">
                    <div class="card-header input-group">
                        <input class="form-control" placeholder="Search" name="srch-term" id="srch-term" type="text">
                        <div class="input-group-btn">
                            <button class="btn btn-default" type="submit">Search</button>
                        </div>
                    </div>
                    <div id="searchresult" class="card-body">
                        Search
                    </div>
                </div>
            </div>
        </div>
    </div>`,
    watch: {
        modelName: {
            immediate: true,
            async handler(val) {
                try {
                    let model = await CyderAPI.Model.get(this.modelName);
                    if(model === undefined) {
                        $.notify({title: `<strong>Not Found:</strong>`, message: "Not Found"},{type: 'danger'});
                        return;
                    }
                    this.model = model;
                } catch(error) {
                    if(!(error instanceof CyderAPI.RESTError))
                        throw(error);
                    notifyRESTError(error);
                }
            },
        },
    },
};
