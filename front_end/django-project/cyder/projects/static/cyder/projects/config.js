'use strict';
import CyderAPI from '../api.js';
import notifyRESTError from '../api-notify-error.js';

export const configPlots = {
    props: {
        p: {},
    },
    data(){
        return {
          loaded: false,
        }
    },
    methods: {
        plot(){

        var load = {
          x: this.p.config.loadIndex,
          y: this.p.config.load,
          name: 'Load',
          type: 'scatter',
          marker: {
                  color: '#0066cc'
                }
        };

        var pv = {
          x: this.p.config.pvIndex,
          y: this.p.config.pv,
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
    template: `
        <div>
          <div v-if="loaded">
            <h5 >Project: {{p.name}}</h5>
            <br>
            <h4>Date: {{p.config.date}}</h4>
            <p>Results are displayed for the day of minimal net load based on scada data and estimated PV Capacity from solar irradiation data.</p>
          </div>
          <br>
          <div id="plotLoad" style="height:70vh;"> </div>
          <div id="plotPV" style="height:70vh;"> </div>
        </div>
        `
}

