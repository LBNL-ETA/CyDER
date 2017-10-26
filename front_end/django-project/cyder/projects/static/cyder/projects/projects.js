class ProjectList extends View {
    constructor(parent) {
        super('div', parent);
        this.projects = [];
        this._getProjects().then((projects) => {
            for(let project of projects)
                this._childs[`project-${project.id}`] = new ProjectItem(this, project);
            this.render();
        });
        this.render();
    }
    _getProjects() {
        if(this._projectsProm)
            return this._projectsProm;
        return this._projectsProm = (async () => {
            this.projects = await CyderAPI.rest('GET', `/api/projects/`);
            return this.projects;
        })();
    }
    update() {
        this._projectsProm = null;
        this._childs = {};
        return this._getProjects().then((projects) => {
            for(let project of projects)
                this._childs[`project-${project.id}`] = new ProjectItem(this, project);
            this.render();
        });
    }
    get _template() {
        return `
        <table class="table table-hover">
            <thead>
                <tr>
                    <th scope="col">#</th>
                    <th scope="col">Name</th>
                    <th scope="col">Model</th>
                    <th scope="col">Status</th>
                    <th scope="col" class="text-right">Action</th>
                </tr>
            </thead>
            <tbody>
                ${ FOREACH(this.projects, (project) =>
                    `<tr data-childview="project-${project.id}"></tr>`
                )}
            </tbody>
        </table>`;
    }
}

class ProjectItem extends View {
    constructor(parent, project) {
        super('tr', parent);
        this.project = project;
        this.render();
    }
    async _onRun(e) {
        await CyderAPI.rest('POST', `/api/projects/${this.project.id}/run/`);
        this.parent.update();
    }
    async _onRevoke(e) {
        await CyderAPI.rest('POST', `/api/projects/${this.project.id}/revoke/`);
        this.parent.update();
    }
    _onResults(e) {
        alert(this.project.result);
    }
    async _onDelete(e) {
        await CyderAPI.rest('DELETE', `/api/projects/${this.project.id}/`);
        this.parent.update();
    }
    get _template() {
        let rowclass = '';
        switch(this.project.status) {
            case 'Succeed':
                rowclass = 'table-success';
                break;
            case 'Failed':
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

        return `
        <th scope="row">${this.project.id}</th>
        <td>${this.project.name}</td>
        <td>${this.project.model}</td>
        <td>${this.project.status}</td>
        <td class="text-right">
            <div class="btn-group" >
                ${IF(this.project.status === 'Pending' || this.project.status === 'Started', () =>
                    `<button type="button" class="btn btn-sm btn-primary" data-on="click:_onRevoke">Revoke</button>`
                , () => IF(this.project.status === 'Succeed', () =>
                    `<button type="button" class="btn btn-sm btn-primary" data-on="click:_onResults">Results</button>`
                , () =>
                    `<button type="button" class="btn btn-sm btn-primary" data-on="click:_onRun">Run simulation</button>`
                ))}
                <button type="button" class="btn btn-sm btn-primary dropdown-toggle dropdown-toggle-split" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                    <span class="sr-only">Toggle Dropdown</span>
                </button>
                <div class="dropdown-menu dropdown-menu-right">
                    <button class="dropdown-item" data-on="click:_onEdit">Edit</button>
                    <button class="dropdown-item" data-on="click:_onDelete">Delete</button>
                </div>
            </div>
        </td>`;
    }
}

let projectList;
window.onload = function() {
    CyderAPI.auth();
    projectList = new ProjectList();
    projectList.emplace(document.querySelector('#project-list'));
    let update = () => { projectList.update(); setTimeout(update, 5000); }
    setTimeout(update, 5000);
}
