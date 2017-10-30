class ProjectEdit extends View {
    constructor(parent) {
        super('div', parent);
        this.project = null;
        this.isNew = null;
    }
    _getProject() {
        if(this._projectProm)
            return this._projectProm;
        else
            return Promise.resolve(this.project);
    }
    loadProject(projectId) {
        this._projectProm = (async () => {
            this.project = await CyderAPI.smartRest('GET', `/api/projects/${projectId}/`);
            this.isNew = false;
            this._projectProm = null;
        })();
        return this._getProject().then(() => { this.render() });
    }
    newProject() {
        this.project = {
            name: '',
            settings: {},
        }
        this.isNew = true;
        this.render();
    }
    render() {
        super.render();
        this._html.name.value = this.project.name;
        this._html.model.value = this.project.settings.model;
    }
    _writeProject() {
        this.project.name = this._html.name.value;
        this.project.settings = {
            model: this._html.model.value,
        }
    }
    async _save(e) {
        this._writeProject();
        await CyderAPI.smartRest('PATCH', `/api/projects/${this.project.id}/`, this.project);
        $.notify({message: 'Project saved !'},{type: 'success'});
    }
    async _create(e) {
        if(e.target.className.indexOf('disable') >= 0)
            return;
        e.target.className += ' disabled';
        this._writeProject();
        this.project = await CyderAPI.smartRest('POST', `/api/projects/`, this.project);
        $.notify({message: 'Project created !'},{type: 'success'});
        this.isNew = false;
        this.render();
        history.replaceState(null, null, `./edit/${this.project.id}`);
    }
    get _template() {
        return `
        <div class="input-group input-group-lg">
            <input data-name="name" type="text" class="form-control" placeholder="Name" aria-label="Name">
        </div><br>
        <div class="input-group input-group-lg">
            <input data-name="model" type="text" class="form-control" placeholder="Model" aria-label="Model">
        </div><br>
        ${ IF(this.isNew, () =>
            `<button type="button" data-on="click:_create" class="btn btn-primary">Create</button>`
        , () =>
            `<button type="button" data-on="click:_save" class="btn btn-primary">Save</button>`
        )}
        `;
    }
}

$.notifyDefaults({
    placement: {
		from: 'bottom',
		align: 'right'
	},
    animate:{
		enter: "animated fadeInDown",
		exit: "animated fadeOutRight"
	},
    type: 'info'
});
