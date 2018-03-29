'use strict';
import { LeafletMap } from '../models/viewer-legacy.js';
import { Layer } from '../models/layers.js';
import CyderAPI from '../api.js';
import notifyRESTError from '../api-notify-error.js';

export const TimestampSelector = {
    props:{ 
        datetimes: null,
    },
    data (){
        return {
            ParsedTimestamp: '',
        }
    },
    methods:{
        parseTimestamp(t){
        return moment(t, "YYYY_MM_DD_HH_mm_ss").toDate().toString();
        },
    },
    watch: {
        ParsedTimestamp : function(newTimestamp, oldTimestamp){
            this.$emit('timestampchanged',moment(this.ParsedTimestamp).format("YYYY_MM_DD_HH_mm_ss"));
        }
    },
    template : `
        <select class="form-control form-control-lg" v-model="ParsedTimestamp">
            <option v-for="t in datetimes" >{{ parseTimestamp(t) }}</option>
        </select>
    `
}



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
}
info.update = function (props) {
    this._div.innerHTML = '<h4> Voltage Details </h4>';
}


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
        index: null,
    },
    data(){
        return {  
            test: null,
        }
    },
    methods: {
        getLayer() {
            let pointToLayer = (feature, latlng) => {
                var circle = L.circle(latlng, {
                    weight: 2,
                    fillOpacity: 1,
                    radius: 3
                });
                circle.bindPopup(this.$refs.popup);
                circle.on('click', () => this.test=feature.properties.vA);
                return circle;
            }
            return L.geoJson(this.geojson, {style: styleA, pointToLayer});
        },
    },
    watch: {
    },
    template: `<div style="display: none;">
        <div ref="popup">
            <h5 v-if="test!=null"> {{test}} pu </h5>
            <h5 v-if="test==null"> unknown </h5>
        </div>
    </div>`
}

export const ResultsLayerB = {
    mixins: [Layer],
    components: {Controller},
    props: {
        geojson: null,
        index: null,
    },
    data(){
        return {
            test: null,
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
                circle.bindPopup(this.$refs.popup);
                circle.on('click', () => this.test=feature.properties.vB);
                return circle;
            }
            return L.geoJson(this.geojson, {style: styleB, pointToLayer});
        },
    },
    template: `<div style="display: none;">
        <div ref="popup">
            <h5 v-if="test!=null"> {{test}} pu </h5>
            <h5 v-if="test==null"> unknown </h5>
        </div>
    </div>`
}

export const ResultsLayerC = {
    mixins: [Layer],
    components: {Controller},
    props: {
        geojson: null,
        index: null,
    },
    data(){
        return {
            test: null,
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
                circle.bindPopup(this.$refs.popup);
                circle.on('click', () => this.test=feature.properties.vC);
                return circle;
            }
            return L.geoJson(this.geojson, {style: styleC, pointToLayer});
        },
    },
    template: `<div style="display: none;">
        <div ref="popup">
            <h5 v-if="test!=null"> {{test}} pu </h5>
            <h5 v-if="test==null"> unknown </h5>
        </div>
    </div>`
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


export const VdPlot = {
    props: {
        results: {},
        timestamp: '',
    },
    data(){
        return {
        vA: [],
        vB: [],
        vC: [],
        distances: [],
        }
    },
    methods: {
        plot(){
            let traceA = {
              x: this.distances,
              y: this.vA,
              mode: 'markers',
              type: 'scatter'
            };

            let data = [traceA];
            var layout = {
              xaxis: {
                title: 'Distance in meters',
                titlefont: {
                  family: 'Courier New, monospace',
                  size: 18,
                  color: '#7f7f7f'
                }
              },
              yaxis: {
                title: 'Voltage in Kw',
                titlefont: {
                  family: 'Courier New, monospace',
                  size: 18,
                  color: '#7f7f7f'
                }
              }
            };

            Plotly.newPlot('plot', data, layout);
        },
        fetchResults(){
             if(this.timestamp!=null && this.results!=null){
                for (let node in this.results[this.timestamp]){
                    this.vA.push(this.results[this.timestamp][node].voltage_A);
                    this.vB.push(this.results[this.timestamp][node].voltage_B);
                    this.vC.push(this.results[this.timestamp][node].voltage_C);
                    this.distances.push(this.results[this.timestamp][node].distance);
                }
            }
        }
    },
    watch: {
        results: function (newResults, oldResults){
            this.fetchResults();
            this.plot();
        },
        index: function (newIndex, oldIndex){
            this.fetchResults();
            this.plot();
        }
    },
    created: function(){
        this.fetchResults();
    },
    mounted: function(){
        this.plot();
    },
    template: '<div id="plot" style="height:70vh;"> </div>'
}