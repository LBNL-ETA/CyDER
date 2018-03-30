'use strict';
import { View, FOREACH, IF, ESCHTML } from '../viewlib.js';
import CyderAPI from '../api.js';
import notifyRESTError from '../api-notify-error.js';


//Still uses Viewlib.js developed by Martin H., this may/should be replaced with ViewJS implementation in later developments

//The following component uses plotly to dipslay two graphs resulting from the scada and solar data located on the CyDER computer


export class ProjectConfig extends View {
    constructor(projectId, el) {
        super(el, 'div');
        this.loadProject(projectId);
    }
    loadProject(projectId, force = false) {
        this._projectId = projectId;
        let prom = CyderAPI.Project.get(this._projectId, force);
        if(prom instanceof Promise) {
            prom.catch((error) => notifyRESTError(error));
            this._ready = prom.then(() => { this.render(); this._plot(); });
        }
        else {
            this._ready = Promise.resolve();
        }
        this.render();
    }
    _plot() {
        let project = CyderAPI.Project.get(this._projectId);

        project.config.pv

        var load = {
          x: project.config.loadIndex,
          y: project.config.load,
          name: 'Load',
          type: 'scatter',
          marker: {
                  color: '#0066cc'
                }
        };

        var pv = {
          x: project.config.pvIndex,
          y: project.config.pv,
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
        Plotly.newPlot(this._html.plotLoad, dataLoad, layoutLoad);
        Plotly.newPlot(this._html.plotPV, dataPV, layoutPV);
    }
    get _template() {
        let project = CyderAPI.Project.get(this._projectId);
        return `
        <h1>Configuration</h1>
        ${ IF(project instanceof Promise, () =>
            `<br>
            Loading...`
        , () =>
            `<h4>Project: ${ESCHTML(project.name)}</h4>
            <br>
            <div data-name="plotLoad" style="height:70vh;"></div>
            <br>
            <div data-name="plotPV" style="height:70vh;"></div>`
        )}
        `;
    }
}
