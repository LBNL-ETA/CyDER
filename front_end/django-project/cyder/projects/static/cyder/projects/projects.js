'use strict';
import { View, FOREACH, IF, ESCHTML } from '../viewlib.js';
import CyderAPI from '../api.js';
import notifyRESTError from '../api-notify-error.js';

export class ProjectList extends View {
    constructor(el) {
        super(el, 'div');
        this.update();
        this.render();
    }
    async update() {
        let projects = await CyderAPI.Project.getAll(true);
        this._childviews = {};
        for(let [projectId, project] of projects)
            this._childviews[`project-${ESCHTML(projectId)}`] = new ProjectItem(project, this);
        this.render();
    }
    get _template() {
        let projects = CyderAPI.Project.getAll();
        return `
        <table class="table table-hover">
            <thead>
                <tr>
                    <th scope="col">#</th>
                    <th scope="col">Name</th>
                    <th scope="col">Stage</th>
                    <th scope="col">Status</th>
                    <th scope="col" class="text-right">Action</th>
                </tr>
            </thead>
            <tbody>
                ${ IF(projects instanceof Promise, () =>
                    `<tr><th></th><td>Loading...</td></tr>`
                , () =>
                    FOREACH(projects.keys(), (projectId) =>
                        `<tr data-childview="project-${ESCHTML(projectId)}"></tr>`
                    )
                )}
            </tbody>
        </table>`;
    }
}

class ProjectItem extends View {
    constructor(project, parentList, el) {
        super(el, 'tr');
        this.project = project;
        this.parentList = parentList;
        this.render();
    }
    async _onAction(e) {
        try {
            await CyderAPI.Project[e.target.dataset.action](this.project.id);
            this.parentList.update();
        } catch(error) {
            if(!(error instanceof CyderAPI.RESTError))
                throw(error);
            notifyRESTError(error);
        }
    }
    _onConfig(e) {
        window.location.href = `./config/${encodeURI(this.project.id)}/`;
    }
    _onResults(e) {
        window.location.href = `./results/${encodeURI(this.project.id)}/`;
    }
    _onEdit(e) {
        window.location.href = `./edit/${encodeURI(this.project.id)}/`;
    }
    render() {
        super.render();
        let rowclass = '';
        switch(this.project.status) {
            case 'Success':
                rowclass = 'table-success';
                break;
            case 'Failure':
                rowclass = 'table-danger';
                break;
            case 'Started':
                rowclass = 'table-primary';
                break;
            case 'Pending':
                rowclass = 'table-secondary';
                break;
        }
        this._html.el.className = rowclass;
    }
    get _template() {
        return `
        <th scope="row">${ESCHTML(this.project.id)}</th>
        <td>${ESCHTML(this.project.name)}</td>
        <td>${ESCHTML(this.project.stage)}</td>
        <td>${ESCHTML(this.project.status)}</td>
        <td class="text-right">
            <div class="btn-group" >
                ${IF(this.project.status === 'Pending' || this.project.status === 'Started', () =>
                    `<button type="button" class="btn btn-sm btn-primary" data-on="click:_onAction" data-action="revoke">Revoke</button>`
                , () => IF(this.project.stage === 'Simulation' && this.project.status === 'Success', () =>
                    `<button type="button" class="btn btn-sm btn-primary" data-on="click:_onResults">Results</button>`
                , () => IF(this.project.stage === 'Simulation' || (this.project.stage === 'Configuration' && this.project.status === 'Success'), () =>
                    `<button type="button" class="btn btn-sm btn-primary" data-on="click:_onAction" data-action="runSim">Run simulation</button>`
                , () =>
                    `<button type="button" class="btn btn-sm btn-primary" data-on="click:_onAction" data-action="runConfig">Run configuration</button>`
                )))}
                <button type="button" class="btn btn-sm btn-primary dropdown-toggle dropdown-toggle-split" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                    <span class="sr-only">Toggle Dropdown</span>
                </button>
                <div class="dropdown-menu dropdown-menu-right">
                    ${ IF(this.project.stage === 'Simulation' || (this.project.stage === 'Configuration' && this.project.status === 'Success'), () =>
                        `<button class="dropdown-item" data-on="click:_onConfig">See configuration</button>
                        <button class="dropdown-item" data-on="click:_onAction" data-action="runConfig">Re-run configuration</button>`
                    )}
                    <button class="dropdown-item" data-on="click:_onEdit">Edit</button>
                    <button class="dropdown-item" data-on="click:_onAction" data-action="delete">Delete</button>
                </div>
            </div>
        </td>`;
    }
}
