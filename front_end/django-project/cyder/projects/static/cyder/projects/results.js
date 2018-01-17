'use strict';
import { View, FOREACH, IF, ESCHTML } from '../viewlib.js';
import CyderAPI from '../api.js';
import notifyRESTError from '../api-notify-error.js';

export class ProjectResults extends View {
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

        let startDate = Date.parse(project.settings.start);
        let endDate = Date.parse(project.settings.end);
        let dates = [];
        for(let date = startDate; date < endDate; date+=project.settings.timestep*1000)
            dates.push(new Date(date));

        let traceHighA = {x: dates, y: project.results.DwHighVoltWorstA, mode: 'lines', name: 'Phase A'};
        let traceHighB = {x: dates, y: project.results.DwHighVoltWorstB, mode: 'lines', name: 'Phase B'};
        let traceHighC = {x: dates, y: project.results.DwHighVoltWorstC, mode: 'lines', name: 'Phase C'};
        let dataHigh = [traceHighA, traceHighB, traceHighC];
        let layoutHigh = {
            title:'Down-line worst high voltage',
            yaxis: {
                title: 'Percentage(%)'
            }
        };
        Plotly.newPlot(this._html.plotHigh, dataHigh, layoutHigh);

        let traceLowA = {x: dates, y: project.results.DwLowVoltWorstA, mode: 'lines', name: 'Phase A'};
        let traceLowB = {x: dates, y: project.results.DwLowVoltWorstB, mode: 'lines', name: 'Phase B'};
        let traceLowC = {x: dates, y: project.results.DwLowVoltWorstC, mode: 'lines', name: 'Phase C'};
        let dataLow = [traceLowA, traceLowB, traceLowC];
        let layoutLow = {
            title:'Down-line worst low voltage',
            yaxis: {
                title: 'Percentage(%)'
            }
        };
        Plotly.newPlot(this._html.plotLow, dataLow, layoutLow);
    }
    get _template() {
        let project = CyderAPI.Project.get(this._projectId);
        return `
        <h1>Results</h1>
        ${ IF(project instanceof Promise, () =>
            `<br>
            Loading...`
        , () =>
            `<h4>Project: ${ESCHTML(project.name)}</h4>
            <br>
            <div data-name="plotHigh" style="height:300px;"></div>
            <div data-name="plotLow" style="height:300px;"></div>`
        )}
        `;
    }
}
