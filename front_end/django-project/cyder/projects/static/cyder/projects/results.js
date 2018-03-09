'use strict';
import { LeafletMap } from '../models/viewer-legacy.js';
import { Layer } from '../models/layers.js';
import CyderAPI from '../api.js';
import notifyRESTError from '../api-notify-error.js';

export const Controller = {
    mixins: [Layer],
    props: {
    },
    data(){
        return {
            I: null,
        }
    },
    methods: {
        async getLayer() {
            return this.I;
        },
    },
}

var info = L.control();
info.onAdd = function (map) {
    this._div = L.DomUtil.create('div', 'info'); // create a div with a class "info"
    this._div.innerHTML = '<h4> Voltage Details </h4>';
    return this._div;
};
info.update = function (props) {
    this._div.innerHTML = '<h4> Voltage Details </h4>';
};





export const LegendLayer = {
    mixins: [Layer],
    props: {
    },
    data(){
        return {
            Le: legend,
        }
    },
    methods: {
        async getLayer() {
            return this.Le;
        },
    },
}

var legend = L.control({position: 'bottomright'});

legend.onAdd = function (map) {

    var div = L.DomUtil.create('div', 'info legend'),
            grades = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            labels = [];

    div.innerHTML =
    '<h5> Voltage Levels</h5>' +
        '<i style="background:' + getColor(1.06) + '"></i>      <i>Over to 5% </i><br>' +
        '<i style="background:' + getColor(1.041) + '"></i>     <i>4% to 5% </i><br>' +
        '<i style="background:' + getColor(1.031) + '"></i>     <i>3% to 4% </i><br>' +
        '<i style="background:' + getColor(1.021) + '"></i>     <i>2% to 3% </i><br>' +
        '<i style="background:' + getColor(1.011) + '"></i>     <i>1% to 2% </i><br>' +
        '<i style="background:' + getColor(1) + '"></i>         <i>-1% to 1% </i><br>' +
        '<i style="background:' + getColor(0.981) + '"></i>     <i>-2% to -1% </i><br>' +
        '<i style="background:' + getColor(0.971) + '"></i>     <i>-3% to -2% </i><br>' +
        '<i style="background:' + getColor(0.961) + '"></i>     <i>-4% to -3% </i><br>' +
        '<i style="background:' + getColor(0.951) + '"></i>     <i>-5% to -4%</i> <br>' +
        '<i style="background:' + getColor(0.9) + '"></i>       <i>Under -5% </i><br>';
        return div;
};




export const ResultsLayerA = {
    mixins: [Layer],
    components: {Controller},
    props: {
        geojson: null,
    },
    data(){
        return {  
            properties: null,    
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
                circle.on("mouseover", () => this.properties=feature.properties.vA);
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
    components: {Controller},
    props: {
        geojson: null,
    },
    data(){
        return {
            properties: null, 
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
                circle.on("mouseover", () => this.properties=feature.properties.vB);
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
    components: {Controller},
    props: {
        geojson: null,
    },
    data(){
        return {
            properties: null, 
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
                circle.on("mouseover", () => this.properties=feature.properties.vC);
                return circle;
            }
            // let highlightFeature = (e)  => {
            //     var layer = e.target;

            //     layer.setStyle({
            //         weight: 5,
            //         color: '#666',
            //         dashArray: '',
            //         fillOpacity: 0.7
            //     });

            //     if (!L.Browser.ie && !L.Browser.opera && !L.Browser.edge) {
            //         layer.bringToFront();
            //     }
            // }
            // let onEachFeature = (feature, layer) => {
            //     layer.on({
            //         mouseover: highlightFeature,
            //         mouseout: resetHighlight,
            //         click: zoomToFeature
            //     });
            // }
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
        case (v<1.05):
            color='#f9600b';
            break;
        case (v>=1.05):
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