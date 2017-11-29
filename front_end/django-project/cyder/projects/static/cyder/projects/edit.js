'use strict';
import { LeafletMap } from '../models/viewer.js';
import { createModelLayer, createPVLayer, createLoadLayer } from '../models/layers.js';


export class CanceledByUser extends Error {}

export class ProjectEditor extends View {
    constructor(el) {
        super(el, 'div');
        this._project = null;
    }
    async loadProject(projectId) {
        this.closeProject();
        this._project = await CyderAPI.Project.get(projectId);
        this._childs['map-editor'] = new ProjectMapEditor(this._project.settings.model);
        this.child('map-editor').addDataLayer('PVs', this._project.settings.addPv, createPVLayer);
        this.child('map-editor').addDataLayer('Loads', this._project.settings.addLoad, createLoadLayer);
        this.child('map-editor').render();
        this._isNew = false;
        this.render();
    }
    closeProject() {
        if(this._project !== null && this.wasModified()) {
            if(!confirm('You have unsaved changes. Continue without saving?'))
                throw new CanceledByUser('User canceled closing the project');
        }
        this._project = null;
    }
    wasModified() {
        if(this._project.name !== this._html.name.value ||
            this._project.settings.start !== this._html.start.value ||
            this._project.settings.end !== this._html.end.value ||
            this._project.settings.timestep !== this._html.timestep.value ||
            this.child('map-editor').dataWasModified('PVs') ||
            this.child('map-editor').dataWasModified('Loads'))
            return true;
        return false;
    }
    async _save(e) {
        if(e.target.classList.contains('disabled'))
            return;
        e.target.classList.add('disabled');
        try {
            this._project.name = this._html.name.value;
            this._project.settings.start = this._html.start.value;
            this._project.settings.end = this._html.end.value;
            this._project.settings.timestep = this._html.timestep.value;
            this._project.settings.addPv = this.child('map-editor').getData('PVs');
            this.child('map-editor').resetDataLayer('PVs');
            this._project.settings.addLoad = this.child('map-editor').getData('Loads');
            this.child('map-editor').resetDataLayer('Loads');
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
        try {
            await this.loadProject(this._project.id);
        } catch(error) {
            if(!(error instanceof CanceledByUser))
                throw error;
        }
        e.target.classList.remove('disabled');
    }
    render() {
        super.render();
        this._html.name.value = this._project.name;
        this._html.start.value = this._project.settings.start;
        this._html.end.value = this._project.settings.end;
        this._html.timestep.value = this._project.settings.timestep;
    }
    get _template() {
        return `
        <div class="form-group">
            <input data-name="name" type="text" class="form-control" placeholder="Name" aria-label="Name">
        </div>
        <div class="row">
            <div class="col-md-5">
                <label>Start: </label>
                <div class="form-group">
                    <input data-name="start" type="datetime-local" class="form-control" placeholder="Start" aria-label="Start">
                </div>
            </div>
            <div class="col-md-5">
                <label>Stop: </label>
                <div class="form-group">
                    <input data-name="end" type="datetime-local" class="form-control" placeholder="End" aria-label="End">
                </div>
            </div>
            <div class="col-md-2">
                <label>Timestep:</label>
                <div class="form-group">
                    <input data-name="timestep" type="number" class="form-control">
                </div>
            </div>
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

export class ProjectMapEditor extends View {
    constructor(modelName, el) {
        super(el, 'div');
        this._childs['leaflet-map'] = new LeafletMap();
        this._dataLayers = {};
        this._currentDataLayer = null;
        this._modelName = modelName;
        this.child('leaflet-map').addLayer(createModelLayer(modelName), 'model');
        this.child('leaflet-map').fitBounds('model');
        this.render();
    }
    addDataLayer(name, data, createLayerFunc) {
        let dataLayer = {};
        dataLayer.map = new Map(data.map(obj => [obj.device, obj.power]));
        dataLayer.map.wasModified = false;
        let bindDevicePopup = (device, marker) => {
            marker.bindPopup((new DevicePopup(device.device_number, marker, dataLayer.map)).el);
        };
        dataLayer.layer = createLayerFunc(this._modelName, bindDevicePopup);
        this._dataLayers[name] = dataLayer;
    }
    resetDataLayer(name) {
        this._dataLayers[name].map.wasModified = false;
    }
    dataWasModified(name) {
        return this._dataLayers[name].map.wasModified;
    }
    getData(name) {
        let map = this._dataLayers[name].map;
        return Array.from(map).map(([device, power]) => ({device, power}));
    }
    _onShowDataLayer(e) {
        let name = e.target.innerHTML;
        let layer = this._dataLayers[name].layer;
        this.child('leaflet-map').removeLayer('dataLayer');
        this.child('leaflet-map').addLayer(this._dataLayers[name].layer, 'dataLayer');
        this._currentDataLayer = name;
        this.render();
    }
    get _template() {
        return `
        <div class="btn-group" role="group">
            ${ FOREACH(this._dataLayers, (name, dataLayer) =>
                IF(name === this._currentDataLayer, () =>
                    `<button type="button" class="btn btn-secondary disabled" data-on="click:_onShowDataLayer">${escapeHtml(name)}</button>`
                , () =>
                    `<button type="button" class="btn btn-secondary" data-on="click:_onShowDataLayer">${escapeHtml(name)}</button>`
                )
            )}
        </div>
        <div data-childview="leaflet-map" style="height: 70vh; margin: 0.1rem 0 1rem 0;"></div>
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
        this._map.wasModified = true;
        this.render();
    }
    _remove(e) {
        this._map.delete(this._number);
        this._map.wasModified = true;
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
