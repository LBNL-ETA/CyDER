'use strict';
import { LeafletMap } from '../models/viewer-legacy.js';
import { Layer } from '../models/layers.js';
import CyderAPI from '../api.js';
import notifyRESTError from '../api-notify-error.js';


export const ResultsLayerA = {
    mixins: [Layer],
    props: {
        geojson: null,
    },
    data(){
        return {
        }
    },
    methods: {
        async getLayer() {
            let pointToLayer = (feature, latlng) => {
                var circle = L.circle(latlng, {
                    weight: 2,
                    fillOpacity: 1,
                    radius: 3
                });
                return circle;
            }
            // let onEachFeature = (feature, layer) => {
            //     feature.setStyle(styleA(feature));
            // }
            return L.geoJson(this.geojson, {style: styleA, pointToLayer});
        },
    },
}

export const ResultsLayerB = {
    mixins: [Layer],
    props: {
        geojson: null,
    },
    data(){
        return {
        }
    },
    methods: {
        async getLayer() {
            let pointToLayer = (feature, latlng) => {
                var circle = L.circle(latlng, {
                    weight: 2,
                    fillOpacity: 1,
                    radius: 3
                });
                return circle;
            }
            // let onEachFeature = (feature, layer) => {
            //     feature.setStyle(styleA(feature));
            // }
            return L.geoJson(this.geojson, {style: styleB, pointToLayer});
        },
    },
}

export const ResultsLayerC = {
    mixins: [Layer],
    props: {
        geojson: null,
    },
    data(){
        return {
        }
    },
    methods: {
        async getLayer() {
            let pointToLayer = (feature, latlng) => {
                var circle = L.circle(latlng, {
                    weight: 2,
                    fillOpacity: 1,
                    radius: 3
                });
                return circle;
            }
            // let onEachFeature = (feature, layer) => {
            //     feature.setStyle(styleA(feature));
            // }
            return L.geoJson(this.geojson, {style: styleC, pointToLayer});
        },
    },
}

function getColor(v) {
    let color;
    switch(v!=null) {
        case (v<=0.95):
            color='#130084';
            break;
        case (v<=0.96):
            color='#1933a4';
            break;
        case (v<=0.97):
            color='#1f88c9';
            break;
        case (v<=0.98):
            color='#4efeb6';
            break;
        case (v<=0.99):
            color='#20eba0';
            break;
        case (v<=1.01):
            color='#32cd32';
            break;
        case (v<=1.02):
            color='#bbff0f';
            break;
        case (v<=1.03):
            color='#fad428';
            break;
        case (v<=1.04):
            color='#f99e28';
            break;
        case (v<=1.05):
            color='#f9600b';
            break;
        case (v>1.05):
            color='#e80101';
            break;
    }
    return color;
}

function styleA (feature) {
    if (feature.properties.vA!=null) {return { color: getColor(feature.properties.vA)};}
    else {return { color: '#808080', opacity: 0.5};}
}
function styleB (feature) {
    if (feature.properties.vB!=null) {return { color: getColor(feature.properties.vB)};}
    else {return { color: '#808080', opacity: 0.5};}
}
function styleC (feature) {
    if (feature.properties.vC!=null) {return { color: getColor(feature.properties.vC)};}
    else {return { color: '#808080', opacity: 0.5};}
}