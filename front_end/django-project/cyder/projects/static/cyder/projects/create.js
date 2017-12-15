'use strict';
import { SelectModel } from '../models/viewer.js';
import { View } from '../viewlib.js';
import CyderAPI from '../api.js';
import notifyRESTError from '../api-notify-error.js';

export class ProjectCreator extends View {
    constructor(el) {
        super(el, 'div');
        this._childviews['select-model'] = new SelectModel(null, false);
        this.render();
    }
    _writeProject() {
        this._project = {
            name: this._html.name.value,
            settings: {
                model: this.childview('select-model').modelName,
                addPv: [],
                addLoad: [],
                start: "2017-05-19T06:00",
                end: "2017-05-19T22:00",
                timestep: 1800,
            },
        };
    }
    async _create(e) {
        if(e.target.classList.contains('disabled'))
            return;
        e.target.classList.add('disabled');
        try {
            this._writeProject();
            this._project = await CyderAPI.Project.create(this._project);
            $.notify({message: 'Project created !'},{type: 'success'});
            window.location.href = `../edit/${encodeURI(this._project.id)}/`;
        } catch (error) {
            if(!(error instanceof CyderAPI.RESTError))
                throw(error);
            notifyRESTError(error);
            e.target.classList.remove('disabled');
        }
    }
    get _template() {
        return `
        <div class="form-group">
            <input data-name="name" type="text" class="form-control" placeholder="Name" aria-label="Name">
        </div>
        <div class="form-group">
            <span data-childview="select-model"></span>
        </div>
        <div class="form-group">
            <button type="button" data-on="click:_create" class="btn btn-primary">Create</button>
        </div>
        `;
    }
}
