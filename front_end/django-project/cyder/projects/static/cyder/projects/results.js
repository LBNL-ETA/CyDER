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



//The implementation of the chloropeth map results visualiser was inspired by: http://leafletjs.com/examples/choropleth/

//Component responsible for displaying the legend on the map
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


//The following three components are responsible displaying voltage results for the selected phase
//The implementations are identical for all three components

//Phase A
export const ResultsLayerA = {
    mixins: [Layer],
    props: {
        geojson: null,
        index: null,
    },
    data(){
        return {  
            popupValue: null,
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
                circle.on('click', () => this.popupValue=feature.properties.vA);
                return circle;
            }
            return L.geoJson(this.geojson, {style: styleA, pointToLayer});
        },
    },
    watch: {
    },
    template: `<div style="display: none;">
        <div ref="popup">
            <h5 v-if="popupValue!=null"> {{popupValue}} pu </h5>
            <h5 v-if="popupValue==null"> unknown </h5>
        </div>
    </div>`
}

//Phase B
export const ResultsLayerB = {
    mixins: [Layer],
    props: {
        geojson: null,
        index: null,
    },
    data(){
        return {
            popupValue: null,
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
                circle.on('click', () => this.popupValue=feature.properties.vB);
                return circle;
            }
            return L.geoJson(this.geojson, {style: styleB, pointToLayer});
        },
    },
    template: `<div style="display: none;">
        <div ref="popup">
            <h5 v-if="popupValue!=null"> {{popupValue}} pu </h5>
            <h5 v-if="popupValue==null"> unknown </h5>
        </div>
    </div>`
}

//Phase C
export const ResultsLayerC = {
    mixins: [Layer],
    props: {
        geojson: null,
        index: null,
    },
    data(){
        return {
            popupValue: null,
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
                circle.on('click', () => this.popupValue=feature.properties.vC);
                return circle;
            }
            return L.geoJson(this.geojson, {style: styleC, pointToLayer});
        },
    },
    template: `<div style="display: none;">
        <div ref="popup">
            <h5 v-if="popupValue!=null"> {{popupValue}} pu </h5>
            <h5 v-if="popupValue==null"> unknown </h5>
        </div>
    </div>`
}


//tool fuction that returns color code corresponding to voltage value v
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

//tool fuctions that will apply in to each geojson feature the style (using getcolor) given the voltage result (contained in the properties fields of the geojson feature)
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

//The following component is responsible for creating and displaying a Voltage/Distance graph for the selected phase
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

//The following component is responsible for creating and displaying a Worst Voltage/Feeder Distance /Time (VFDT) 
export const Vfdt = {
    props: {
        results: {},
        datetimes: null,
    },
    data(){
        return {
        worstHighVoltages: [],
        worstLowVoltages:[],
        distancesHigh: [],
        distancesLow: [],
        times:[],
        }
    },
    methods: {
        plot(){
            let xValues = this.times;

            let yValuesHigh = this.worstHighVoltages;

            let yValuesLow = this.worstLowVoltages;

            let traceHigh = {
                  x: xValues,
                  y: yValuesHigh,
                  name: 'Worst High Votages',
                  autobinx: true, 
                  histnorm: "count", 
                  marker: {
                    color: "rgba(255, 100, 102, 0.7)", 
                     line: {
                      color:  "rgba(255, 100, 102, 1)", 
                      width: 1
                    }
                  },  
                  opacity: 0.5, 
                  type: "bar", 
                };

            let traceLow = {
                  x: xValues,
                  y: yValuesLow, 
                  autobinx: true, 
                  marker: {
                          color: "rgba(100, 200, 102, 0.7)",
                           line: {
                            color:  "rgba(100, 200, 102, 1)", 
                            width: 1
                    } 
                       }, 
                  name: "Worst Low Voltages", 
                  opacity: 0.75, 
                  type: "bar", 
                };
            var data = [traceHigh, traceLow];
            var layout = {
                  barmode: "overlay", 
                  title: "Worst High and Low Voltages in Time",  
                  yaxis: {title: "Worst High Low Voltages in pu"}
                };
            Plotly.newPlot('VFDTplot', data, layout);
        },
        fetchData(){
            for (let timestamp in this.results){
                this.worstHighVoltages.push(this.results[timestamp]['worstHighVoltage'].max);
                this.worstLowVoltages.push(this.results[timestamp]['worstLowVoltage'].min);
                this.times.push(timestamp);
            }
        }
    },
    watch: {
    },
    created: function(){
        this.fetchData();
    },
    mounted: function(){
        this.plot();
    },
    template: '<div id="VFDTplot" style="height:80vh;"> </div>'
}