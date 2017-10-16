function getJSON(url) {
    return new Promise(function(resolve, reject) {
        var xhr = new XMLHttpRequest();
        xhr.open('GET', url, true);
        xhr.responseType = 'json';
        xhr.onload = function() {
            if (xhr.status === 200) {
                resolve(xhr.response);
            } else {
                reject(xhr);
            }
        };
        xhr.send();
    });
}

class SelectModel extends View {
    constructor(parent) {
        super('span', parent);
        this.models = [];
        this.getModels().then((models) => {
            this.models = models;
            this.render();
        });
        this.render();
    }
    _onchange(e) {
        this.parent.modelName = this._html.select.value;
    }
    getModels() {
        return this.parent.getModels();
    }
    get _template() {
        return `
        Select a model to display: <select data-name="select" data-on="change:_onchange" class="custom-select">
            <option value="">All</option>
            ${ FOREACH(this.models, (modelName) =>
                `<option value"${modelName}">${modelName}</option>`
            )}
        </select>`;
    }
    set modelName(val) { this.getModels().then(() => this._html.select.value = val); }
}

class LeafletMap extends View {
    constructor(el) {
        super('div', el);
        this.render();
    }
    render() {
        super.render();
        this.map = L.map(this._html.el).setView([37.8,-122.0], 9);
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            maxZoom: 19,
            attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
        }).addTo(this.map);
    }
    emplace(el) {
        super.emplace(el);
        this.map.invalidateSize();
    }
}

class ModelPopup extends View {
    constructor(parent, modelName) {
        super('div', parent);
        this.modelName = modelName;
        this.render();
    }
    _onclick(e) {
        this.parent.modelName = this.modelName;
    }
    get _template() {
        return `
        ${this.modelName}<br>
        <button class='btn btn-primary btn-sm' data-on="click:_onclick">Open</button>`;
    }
}

class ModelViewer extends View {
    constructor(el) {
        super('div',el);
        this.getModels();
        this._childs['select-model'] = new SelectModel(this);
        this._childs['leaflet-map'] = new LeafletMap(this);
        this._childs['model-info'] = new ModelInfo(this, this.child('leaflet-map').map);
    }
    get modelName() { return this._modelName; }
    set modelName(newModelName) {
        if(newModelName === this._modelName)
            return;
        if(this._modelName === '')
            this._getAllModelsLayer().then((layer) => layer.remove());
        this._modelName = newModelName;
        if (this._modelName === '') {
            this._getAllModelsLayer().then((layer) => {
                layer.addTo(this.child('leaflet-map').map);
                this.child('leaflet-map').map.fitBounds(layer.getBounds());
            });
            this.child('model-info').model = null;
        } else {
            this.getModels().then((models) =>
                this.child('model-info').model = models[this._modelName]);
        }
        this.child('select-model').modelName = this._modelName;
        history.replaceState(null, null, `./${this._modelName}`);
    }
    getModels() {
        if(this._modelsProm)
            return this._modelsProm;
        return this._modelsProm = (async () => {
            let models = await getJSON('/api/models');
            models = models.reduce((obj, model) => {obj[model.name] = model; return obj;}, {});
            for(let modelName in models)
                models[modelName].nodes = {};
            return models;
        })();
    }
    _getAllModelsLayer() {
        if (this._allModelsLayerProm)
            return this._allModelsLayerProm;
        return this._allModelsLayerProm = (async () => {
            let geojson = await getJSON('/api/models/geojson');
            let onEachFeature = (feature, layer) => {
                let popup = new ModelPopup(this, feature.properties.modelname);
                layer.bindPopup(popup.el);
            }
            return L.geoJson(geojson, {
                onEachFeature: onEachFeature
            });
        })();
    }
    get _template() {
        return `
        <div data-childview="select-model"></div>
        <div data-childview="leaflet-map" style="height: 70vh; margin: 1rem 0 1rem 0;"></div>
        <div data-childview="model-info"></div>`;
    }
}

class ModelInfo extends View {
    constructor(parent, map) {
        super('div', parent);
        this._map = map;
    }
    get model() { return this._model; }
    set model(model) {
        if(this._model)
            this._getModelLayer().then((layer) => layer.remove());
        this._model = model;
        if(this._model !== null)
            this._getModelLayer().then((layer) => {
                layer.addTo(this._map);
                this._map.fitBounds(layer.getBounds());
            });
        this.render();
    }
    _getModelLayer() {
        if(!this.model)
            throw "Can't get the model layer: No model givem to ModelInfo";
        if(this.model.layerProm)
            return this.model.layerProm;
        return this.model.layerProm = (async () => {
            let geojson = await getJSON(`/api/models/${this.model.name}/geojson`);
            let pointToLayer = (feature, latlng) => {
                var circle = L.circle(latlng, {
                    color: 'red',
                    weight: 2,
                    fillOpacity: 1,
                    radius: 3
                });
                circle._leaflet_id = feature.properties.id;
                circle.on('click', (e) => { this._onNodeClick(e); });
                return circle;
            }
            return L.geoJson(geojson, {
                pointToLayer: pointToLayer
            });
        })();
    }
    async _onNodeClick(e) {
        let node = this.model.nodes[e.target._leaflet_id];
        if(!node) {
            node = await getJSON(`/api/models/${this.model.name}/nodes/${e.target._leaflet_id}`);
            this.model.nodes[node.node_id] = node;
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

let modelViewer;
window.onload = function() {
    modelViewer = new ModelViewer();
    modelViewer.emplace(document.querySelector('#model-viewer'));
    modelViewer.render();
    modelViewer.modelName = djangoContext.modelName;
}
