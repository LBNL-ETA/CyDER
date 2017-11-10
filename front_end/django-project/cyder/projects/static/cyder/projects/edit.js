'use strict';

class ProjectEditor extends View {
    constructor(el) {
        super(el, 'div');
        this._childs['leaflet-map'] = new LeafletMap();
        this._project = null;
        this._addPvMap;
    }
    async loadProject(projectId) {
        this._project = await CyderAPI.Project.get(projectId);
        this._addPvMap = new Map(this._project.settings.addPv.map(obj => [obj.device, obj.power]));
        this._isNew = false;
        this.render();
        this._loadMapLayers(this._project.settings.model);
    }
    _loadMapLayers(modelName) {
        this.child('leaflet-map').removeLayers();
        let modelLayer = createModelLayer(modelName);
        let addPVPopup = (pv, marker) => {
            marker.bindPopup((new PVPopup(pv.device_number, marker, this._addPvMap)).el);
        };
        let pvLayer = createPVLayer(modelName, addPVPopup);
        this.child('leaflet-map').addLayer(modelLayer, 'base');
        this.child('leaflet-map').addLayer(pvLayer, 'pvs', true);
        this.child('leaflet-map').fitBounds('base');
    }
    _writeProject() {
        this._project.name = this._html.name.value;
        this._project.settings.addPv = Array.from(this._addPvMap).map(([device, power]) => ({device, power}));
    }
    async _save(e) {
        if(e.target.classList.contains('disabled'))
            return;
        e.target.classList.add('disabled');
        try {
            this._writeProject();
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
        <div data-childview="leaflet-map" style="height: 70vh; margin: 1rem 0 1rem 0;"></div>
        <div class="form-group">
            <button type="button" data-on="click:_save" class="btn btn-primary">Save</button>
            <button type="button" data-on="click:_cancel" class="btn btn-primary">Cancel</button>
        </div>
        `;
    }
}

class PVPopup extends View {
    constructor(pvNumber, marker, addPvMap) {
        super(null, 'div');
        this._pvNumber = pvNumber;
        this._marker = marker;
        this._addPvMap = addPvMap;
        this.render();
    }
    _set(e) {
        let power = Number(this._html.power.value);
        if(Number.isNaN(power) || this._html.power.value === '') {
            $.notify({ message: 'Power must be a number'}, {type: 'danger'});
            return;
        }
        this._addPvMap.set(this._pvNumber, power);
        this.render();
    }
    _remove(e) {
        this._addPvMap.delete(this._pvNumber);
        this.render();
    }
    render() {
        super.render();
        if(this._addPvMap.has(this._pvNumber)) {
            this._marker.setStyle({color: '#14e54c'});
            this._html.power.value = this._addPvMap.get(this._pvNumber);
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
        ${ IF(this._addPvMap.has(this._pvNumber), () =>
            `<button type="button" data-on="click:_remove" class="btn btn-primary btn-sm">Remove</button>`
        )}`;
    }
}
