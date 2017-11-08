class SelectModel extends View {
    constructor(el, allowEmpty = true) {
        super(el, 'span');
        this.allowEmpty = allowEmpty;
        let prom = CyderAPI.Model.getAll();
        if(prom instanceof Promise)
            this._ready = prom.then(() => { this.render() });
        else
            this._ready = Promise.resolve();
        this.render();
    }
    reloadModels() {
        return this._ready = CyderAPI.Model.getAll(true)
            .then(() => { this.render(); });
    }
    get ready() { return this._ready; }
    onchange(e) {}
    get _template() {
        let models = CyderAPI.Model.getAll();
        return `
        <select data-name="select" data-on="change:onchange" class="custom-select">
            ${ IF(this.allowEmpty, () => `<option value=""></option>` )}
            ${ IF(!(models instanceof Promise), () =>
                FOREACH(models, (model) =>
                    `<option value"${model}">${model}</option>`
                )
            )}
        </select>`;
    }
    get modelName() { return this._html.select.value }
    set modelName(val) { this.ready.then(() => this._html.select.value = val); }
}

class LeafletMap extends View {
    constructor(el) {
        super(el, 'div');
        LeafletMap.addStyle();
        this._layers = {};
        this._loadingLayers = 0;
        this.render();
    }
    _updateLoadingLayers(val) {
        this._loadingLayers += val;
        if(this._loadingLayers > 0)
            this._html.loading.style.display = "block";
        else
            this._html.loading.style.display = "none";
    }
    render() {
        super.render();
        this._map = L.map(this._html.el).setView([37.8,-122.0], 9);
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            maxZoom: 19,
            attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
        }).addTo(this._map);
    }
    get _template() {
        return `
        <div data-name="loading" class="leaflet-loading" style="display: none"></div>`
    }
    emplace(el) {
        super.emplace(el);
        this._map.invalidateSize();
    }
    get map() { return this._map; }
    async addLayer(layer, name) {
        this._layers[name] = layer;
        if(layer instanceof Promise) {
            let layerProm = layer;
            this._updateLoadingLayers(+1);
            layer = await layerProm;
            if(this._layers[name] !== layerProm)
                return false; // The layer have been removed while loading
            this._layers[name] = layer;
            this._updateLoadingLayers(-1);
        }
        layer.addTo(this._map);
        return true;
    }
    removeLayer(name) {
        let layer = this._layers[name];
        delete this._layers[name];
        if(layer instanceof Promise)
            this._updateLoadingLayers(-1);
        else
            layer.remove();
    }
    removeLayers() {
        for(let layerName in this._layers)
            this.removeLayer(layerName);
    }
    async fitBounds(name) {
        let layer = this._layers[name];
        if(layer instanceof Promise) {
            let layerProm = layer;
            layer = await layerProm;
            if(layer !== this._layers[name])
                return false; // The layer have been removed while loading
        }
        this._map.fitBounds(layer.getBounds());
        return true;
    }
}
LeafletMap.addStyle = function() {
    if(LeafletMap._style)
        return;
    LeafletMap._style = document.createElement('style');
    LeafletMap._style.appendChild(document.createTextNode(`
        .leaflet-loading {
            float: right;
            position:relative;
            opacity: 0.7;
            background-color: #FFF;
            background-image: url("/static/cyder/loading.gif");
            background-repeat: no-repeat;
            width: 55px;
            height: 55px;
            z-index: 500;
        }
        `));
    document.getElementsByTagName('head')[0].appendChild(LeafletMap._style);
}

class OpenModelPopup extends View {
    constructor(modelName, modelViewer) {
        super(null, 'div');
        this.modelName = modelName;
        this.modelViewer = modelViewer;
        this.render();
    }
    onopen(e) {
        this.modelViewer.modelName = this.modelName;
    }
    get _template() {
        return `
        ${this.modelName}<br>
        <button class='btn btn-primary btn-sm' data-on="click:onopen">Open</button>`;
    }
}

class ModelViewer extends View {
    constructor(url, el) {
        super(el, 'div');
        this.url = url;
        this._childs['select-model'] = new SelectModel();
        this.child('select-model').onchange = (e) => {
            this.modelName = this.child('select-model').modelName;
        };
        this._childs['leaflet-map'] = new LeafletMap();
        this._childs['model-info'] = new ModelInfo(this.child('leaflet-map'));
    }
    get modelName() { return this._modelName; }
    set modelName(newModelName) {
        if(newModelName === this._modelName)
            return;
        if(this._modelName !== undefined && this._modelName === '')
            this.child('leaflet-map').removeLayer('allModel');
        this._modelName = newModelName;
        if (this._modelName === '') {
            this.child('leaflet-map').addLayer(this._getAllModelsLayer(), 'allModel');
            this.child('leaflet-map').fitBounds('allModel');
            this.child('model-info').model = null;
            history.replaceState(null, null, this.url);
        } else {
            Promise.resolve(CyderAPI.Model.getAll()).then((models) =>
                this.child('model-info').model = models[this._modelName]);
            history.replaceState(null, null, `${this.url}${this._modelName}/`);
        }
        this.child('select-model').modelName = this._modelName;
    }
    _getAllModelsLayer() {
        if (this._allModelsLayerProm)
            return this._allModelsLayerProm;
        let addModelPopup = (feature, layer) => {
            let popup = new OpenModelPopup(feature.properties.modelname, this);
            layer.bindPopup(popup.el);
        };
        return this._allModelsLayerProm = createAllModelsLayer(addModelPopup);
    }
    get _template() {
        return `
        Select a model to display: <span data-childview="select-model"></span>
        <div data-childview="leaflet-map" style="height: 70vh; margin: 1rem 0 1rem 0;"></div>
        <div data-childview="model-info"></div>`;
    }
}

class ModelInfo extends View {
    constructor(leafletMap, el) {
        super(el, 'div');
        this._leafletMap = leafletMap;
    }
    get model() { return this._model; }
    set model(model) {
        if(this._model)
            this._leafletMap.removeLayer('model');
        this._model = model;
        if(this._model !== null) {
            this._leafletMap.addLayer(this._getModelLayer(), 'model');
            this._leafletMap.fitBounds('model');
        }
        this.render();
    }
    _getModelLayer() {
        if(!this.model)
            throw "Can't get the model layer: No model given to ModelInfo";
        if(this.model.layerProm)
            return this.model.layerProm;
        let addNodePopup = (feature, layer) => {
            if(feature.geometry.type !== 'Point')
                return;
            layer._leaflet_id = feature.properties.id;
            layer.on('click', (e) => { this._onNodeClick(e); });
        }
        return this.model.layerProm = createModelLayer(this.model.name, addNodePopup);
    }
    async _onNodeClick(e) {
        if(!e.target.getPopup()) {
            let node = await CyderAPI.Node.get(this.model.name, e.target._leaflet_id);
            var display = (num) => (num == null) ? "NA" : num;
            e.target.bindPopup(
                `Node ${node.node_id}<br>
                VoltageA: ${display(node.VA)}<br>
                VoltageB: ${display(node.VB)}<br>
                VoltageC: ${display(node.VC)}`);
            e.target.openPopup();
        }
    }
    get _template() {
        return `${ IF(this.model, () =>
            `<div class="row" style="margin-bottom: 1rem">
                <div class=col-md-4>
                    <div class="card">
                        <div class="card-header">
                            Infos
                        </div>
                        <div class="card-body">
                            Model name: ${ this.model.name }<br>
                            Nodes count: <span id="nodescount"></span><br>
                            Devices count: <span id="devicescount"></span><br>
                        </div>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="card">
                        <div class="card-header">
                            Devices count detail
                        </div>
                        <div id="devicecountdetail" class="card-body">

                        </div>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="card">
                        <div class="card-header input-group">
                            <input class="form-control" placeholder="Search" name="srch-term" id="srch-term" type="text">
                            <div class="input-group-btn">
                                <button class="btn btn-default" type="submit">Search</button>
                            </div>
                        </div>
                        <div id="searchresult" class="card-body">
                            Search
                        </div>
                    </div>
                </div>
            </div>`
        ) }`;
    }
}

async function createAllModelsLayer(onEachFeature = ()=>{}) {
    let geojson = await CyderAPI.rest('GET', '/api/models/geojson/');
    return L.geoJson(geojson, {
        onEachFeature
    });
}
async function createModelLayer(modelName, onEachFeature = ()=>{}) {
    let geojson = await CyderAPI.rest('GET', `/api/models/${modelName}/geojson/`);
    let pointToLayer = (feature, latlng) => {
        var circle = L.circle(latlng, {
            color: 'red',
            weight: 2,
            fillOpacity: 1,
            radius: 3
        });
        return circle;
    }
    return L.geoJson(geojson, {
        pointToLayer,
        onEachFeature
    });
}
/*async function createPVLayer(modelName, onEachFeature = ()=>{}) {
    let pvs = await CyderAPI.Device.getAll(modelName)
        .filter((device) => device.device_type == 39);
    let layer = L.layerGroup([]);
    for(device)
    return layer;
}*/
