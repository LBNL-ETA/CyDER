'use strict';
import { View, FOREACH, IF, ESCHTML } from '../viewlib.js';
import CyderAPI from '../api.js';
import notifyRESTError from '../api-notify-error.js';

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
          type: 'scatter'
        };

        var pv = {
          x: project.config.pvIndex,
          y: project.config.pv,
          name: 'PV',
          yaxis: 'y2',
          type: 'scatter'
        };

        let data = [load, pv];
        let layout = {
                yaxis: {title: 'Load in KW'},
                yaxis2: {
                    title: 'PV in KW',
                    overlaying: 'y',
                    side: 'right'
                }
        };
        Plotly.newPlot(this._html.plot, data, layout);
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
            <div data-name="plot" style="height:70vh;"></div>`
        )}
        `;
    }
}
