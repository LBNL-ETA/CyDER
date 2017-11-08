class ProjectList extends View {
    constructor(el) {
        super(el, 'div');
        this.update();
        this.render();
    }
    async update() {
        let projects = await CyderAPI.Project.getAll(true);
        this._childs = {};
        for(let [projectId, project] of projects)
            this._childs[`project-${projectId}`] = new ProjectItem(project, this);
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
                    <th scope="col">Status</th>
                    <th scope="col" class="text-right">Action</th>
                </tr>
            </thead>
            <tbody>
                ${ IF(projects instanceof Promise, () =>
                    `<tr><th></th><td>Loading...</td></tr>`
                , () =>
                    FOREACH(projects.keys(), (projectId) =>
                        `<tr data-childview="project-${projectId}"></tr>`
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
    async _onRun(e) {
        await CyderAPI.Project.run(this.project.id);
        this.parentList.update();
    }
    async _onRevoke(e) {
        await CyderAPI.Project.revoke(this.project.id);
        this.parentList.update();
    }
    _onResults(e) {
        window.location.href = `./results/${this.project.id}/`
    }
    _onEdit(e) {
        window.location.href = `./edit/${this.project.id}/`
    }
    async _onDelete(e) {
        await CyderAPI.Project.delete(this.project.id);
        this.parentList.update();
    }
    render() {
        super.render();
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
    }
    get _template() {
        return `
        <th scope="row">${this.project.id}</th>
        <td>${this.project.name}</td>
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
