'use strict';

class CanceledByUser extends Error {}

class ProjectEditor extends View {
    constructor(el) {
        super(el, 'div');
        this._project = null;
    }
    async loadProject(projectId) {
        this.closeProject();
        this._project = await CyderAPI.Project.get(projectId);
        this._childs['map-editor'] = new ProjectMapEditor(this._project.settings.model);
        this.child('map-editor').addPv = this._project.settings.addPv;
        this._isNew = false;
        this.render();
    }
    closeProject() {
        if(this._project !== null && this.hasChanges()) {
            if(!confirm('You have unsaved changes. Continue without saving?'))
                throw new CanceledByUser('User canceled closing the project');
        }
        this._project = null;
    }
    hasChanges() {
        if(this._project.name !== this._html.name.value)
            return true;
        if(this.child('map-editor').addPvIsDirty)
            return true;
        return false;
    }
    async _save(e) {
        if(e.target.classList.contains('disabled'))
            return;
        e.target.classList.add('disabled');
        try {
            if(this._project.name !== this._html.name.value)
                this._project.name = this._html.name.value;
            if(this.child('map-editor').addPvIsDirty)
                this._project.settings.addPv = this.child('map-editor').addPv;
            this._project = await CyderAPI.Project.update(this._project.id, this._project);
            $.notify({message: 'Project saved !'},{type: 'success'});
            this.render();
        } catch(error) {
            if(!(error instanceof CyderAPI.Error))
                throw(error);
            error.notify();
        }
        e.target.classList.remove('disabled');
    }
    async _cancel(e) {
        if(e.target.classList.contains('disabled'))
            return;
        e.target.classList.add('disabled');
        await this.loadProject(this._project.id);
        e.target.classList.remove('disabled');
    }
    render() {
        super.render();
        this._html.name.value = this._project.name;
    }
    get _template() {
        return `
        <div class="form-group">
            <input data-name="name" type="text" class="form-control" placeholder="Name" aria-label="Name">
        </div>
        Model: ${escapeHtml(this._project.settings.model)}<br>
        <div data-childview="map-editor"></div>
        <div class="form-group">
            <button type="button" data-on="click:_save" class="btn btn-primary">Save</button>
            <button type="button" data-on="click:_cancel" class="btn btn-primary">Cancel</button>
        </div>
        `;
    }
}

class ProjectMapEditor extends View {
    constructor(modelName, el) {
        super(el, 'div');
        this._childs['leaflet-map'] = new LeafletMap();
        this._addPvMap;
        this._modelName = modelName;
        this.child('leaflet-map').addLayer(createModelLayer(modelName), 'model');
        this.child('leaflet-map').fitBounds('model');
        this.render();
    }
    set addPv(val) {
        this._addPvMap = new Map(val.map(obj => [obj.device, obj.power]));
        this._addPvMap.isDirty = false;
        this.child('leaflet-map').removeLayer('pvs');
        this.child('leaflet-map').addLayer(this._createPvLayer(this._modelName), 'pvs', true);
    }
    get addPv() {
        return Array.from(this._addPvMap).map(([device, power]) => ({device, power}));
    }
    get addPvIsDirty() { return this._addPvMap.isDirty; }
    _createPvLayer(modelName) {
        let addPvPopup = (pv, marker) => {
            marker.bindPopup((new DevicePopup(pv.device_number, marker, this._addPvMap)).el);
        };
        return createPVLayer(modelName, addPvPopup);
    }

    get _template() {
        return `
        <div data-childview="leaflet-map" style="height: 70vh; margin: 1rem 0 1rem 0;"></div>
        `;
    }
    emplace(el) {
        super.emplace(el);
        this.child('leaflet-map').map.invalidateSize();
    }
}

class DevicePopup extends View {
    constructor(number, marker, map) {
        super(null, 'div');
        this._number = number;
        this._marker = marker;
        this._map = map;
        this.render();
    }
    _set(e) {
        let power = Number(this._html.power.value);
        if(Number.isNaN(power) || this._html.power.value === '') {
            $.notify({ message: 'Power must be a number'}, {type: 'danger'});
            return;
        }
        this._map.set(this._number, power);
        this._map.isDirty = true;
        this.render();
    }
    _remove(e) {
        this._map.delete(this._number);
        this._map.isDirty = true;
        this.render();
    }
    render() {
        super.render();
        if(this._map.has(this._number)) {
            this._marker.setStyle({color: '#14e54c'});
            this._html.power.value = this._map.get(this._number);
        }
        else
            this._marker.setStyle({color: '#3388ff'});
    }
    get _template() {
        return `
        <div class="form-group" style="width:200px;">
            <input data-name="power" type="number" class="form-control form-control-sm" placeholder="Power" aria-label="Power">
        </div>
        <button type="button" data-on="click:_set" class="btn btn-primary btn-sm">Set</button>
        ${ IF(this._map.has(this._number), () =>
            `<button type="button" data-on="click:_remove" class="btn btn-primary btn-sm">Remove</button>`
        )}`;
    }
}
