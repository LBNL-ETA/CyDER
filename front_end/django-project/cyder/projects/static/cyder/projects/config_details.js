'use strict';
import CyderAPI from '../api.js';
import notifyRESTError from '../api-notify-error.js';

export const DateSelector = {
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
        return moment(t, "YYYY-MM-DD").toDate().toDateString();
        },
    },
    watch: {
        ParsedTimestamp : function(newTimestamp, oldTimestamp){
            this.$emit('timestampchanged',moment(this.ParsedTimestamp).format("YYYY-MM-DD"));
        }
    },
    template : `
        <select class="form-control form-control-lg" v-model="ParsedTimestamp">
            <option v-for="t in datetimes" >{{ parseTimestamp(t) }}</option>
        </select>
    `
}

export const configPlots = {
    props: {
        d: {},
        timestamp: '',
    },
    data(){
        return {
          loaded: false,
        }
    },
    methods: {
        plot(){

        var load = {
          x: this.d[this.timestamp].loadIndex,
          y: this.d[this.timestamp].load,
          name: 'Load',
          type: 'scatter',
          marker: {
                  color: '#0066cc'
                }
        };

        var pv = {
          x: this.d[this.timestamp].pvIndex,
          y: this.d[this.timestamp].pv,
          name: 'PV',
          type: 'scatter',
          marker: {
                  color: '#009933'
                }
        };

        let dataLoad = [load];
        let dataPV = [pv];
        let layoutLoad = {
                title: 'Load in Time',
                yaxis: {
                    title: 'Load in KW'
                },
        };
         let layoutPV = {
                title: 'PV capacity in Time',
                yaxis: {title: 'PV in KW'},
        };
        Plotly.newPlot('plotLoad', dataLoad, layoutLoad);
        Plotly.newPlot('plotPV', dataPV, layoutPV);
        },
    },
    watch: {
        p: function (newP, oldP){
            this.loaded=true;
            this.plot();
        },
    },
    mounted: function(){
        this.plot();
    },
    template: `
        <div>
          <div v-if="loaded">
            
            <br>
            <h4>Date: {{timestamp}} </h4>
            <p>Results are displayed</p>
          </div>
          <br>
          <div id="plotLoad" style="height:70vh;"> </div>
          <div id="plotPV" style="height:70vh;"> </div>
        </div>
        `
}