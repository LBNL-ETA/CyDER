'use strict';
import CyderAPI from '../api.js';

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
        <select @change="$emit('change', $event.target.value)" :value="value" class="custom-select" :disabled="isLoading">
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
        this.$data._layers = new Map();
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
