'use strict';

class ProjectResults extends View {
    constructor(projectId, el) {
        super(el, 'div');
        this.loadProject(projectId);
    }
    loadProject(projectId, force = false) {
        this._projectId = projectId;
        let prom = CyderAPI.Project.get(this._projectId, force);
        if(prom instanceof Promise)
            this._ready = prom.then(() => { this.render(); this._plot(); });
        else
            this._ready = Promise.resolve();
        this.render();
    }
    _plot() {
        let project = CyderAPI.Project.get(this._projectId);

        let startTime = Date.parse(project.settings.start);
        let times = [];

        let traceHighA = {x: times, y: [], mode: 'lines', name: 'Phase A'};
        let traceHighB = {x: times, y: [], mode: 'lines', name: 'Phase B'};
        let traceHighC = {x: times, y: [], mode: 'lines', name: 'Phase C'};
        let traceLowA = {x: times, y: [], mode: 'lines', name: 'Phase A'};
        let traceLowB = {x: times, y: [], mode: 'lines', name: 'Phase B'};
        let traceLowC = {x: times, y: [], mode: 'lines', name: 'Phase C'};

        for(let i = 0; i < project.results.length; i++) {
            times.push(new Date(startTime+project.results[i].time*1000));
            traceHighA.y.push(project.results[i].DwHighVoltWorstA);
            traceHighB.y.push(project.results[i].DwHighVoltWorstB);
            traceHighC.y.push(project.results[i].DwHighVoltWorstC);
            traceLowA.y.push(project.results[i].DwLowVoltWorstA);
            traceLowB.y.push(project.results[i].DwLowVoltWorstB);
            traceLowC.y.push(project.results[i].DwLowVoltWorstC);
        }

        let dataHigh = [traceHighA, traceHighB, traceHighC];
        let layoutHigh = {
            title:'DwHighVoltWorst'
        };
        Plotly.newPlot(this._html.plotHigh, dataHigh, layoutHigh);

        let dataLow = [traceLowA, traceLowB, traceLowC];
        let layoutLow = {
            title:'DwLowVoltWorst'
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
            `<h4>Project: ${escapeHtml(project.name)}</h4>
            <br>
            <div data-name="plotHigh" style="height:300px;"></div>
            <div data-name="plotLow" style="height:300px;"></div>`
        )}
        `;
    }
}
