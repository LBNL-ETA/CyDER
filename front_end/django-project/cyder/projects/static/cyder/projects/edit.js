'use strict';
import { LeafletMap } from '../models/viewer-legacy.js';
import { Layer, createPVLayer, createLoadLayer } from '../models/layers.js';
import { View, FOREACH, IF, ESCHTML } from '../viewlib.js';
import CyderAPI from '../api.js';
import notifyRESTError from '../api-notify-error.js';



export const AddPvLayer = {
    mixins: [Layer],
    props: {
        modelName: null,
        value: { required: true, default() { return [];}, }, 
        selectedFeeders: null,
        geojson: null,
    },
    data(){
        return {
            selectedNode: null,
            selectedFeeder:null,
            power: null,
            currentMarker: null,
            exists: null,
            test: null,
        }
    },
    methods: {
        async getLayer() {
            let geojson = {
                'features' : [],
                'type': 'FeatureCollection'
            }
            for (let i=0; i<this.selectedFeeders.length; i++){
                geojson.features=geojson.features.concat(this.geojson[ this.selectedFeeders[i] ]);
            }
            this.test=geojson;
            let pointToLayer = (feature, latlng) => {
                var circle = L.circle(latlng, {
                    color: 'red',
                    weight: 2,
                    fillOpacity: 1,
                    radius: 5
                });
                circle.bindPopup(this.$refs.popup);
                circle.on("click", () => this.selectedNode=feature.properties.id);
                circle.on("click", () => this.selectedFeeder=feature.properties.feeder);
                circle.on("click", () => this.currentMarker=circle);
                circle.on("click", () => this.checkExists());

                for (let i=0; i<this.value.length; i++){
                    if (this.value[i].node_id===feature.properties.id){
                        circle.setStyle({color: '#14e54c'});
                    }
                }

                return circle;
                }
            return L.geoJson(geojson, {
                pointToLayer,
                //onEachFeature
            });
        },

        addPV(){
            if (this.power!=null){
                let valueObject= { 
                        node_id: this.selectedNode,
                        feeder: this.selectedFeeder,
                        power: this.power, 
                    };
                this.value.push(valueObject);
                this.currentMarker.setStyle({color: '#14e54c'});
            }
            this.checkExists();
            $.notify({message: 'PV Added !'},{type: 'success'});

        },
        removePV(){
                let nodeID=this.selectedNode;
                for (let i=0; i<this.value.length; i++){
                    if (this.value[i].node_id===nodeID){
                        this.value.splice(i, 1);
                    }
                }
                this.currentMarker.setStyle({color: 'red'});
                this.checkExists();
                $.notify({message: 'PV Removed !'},{type: 'warning'});  
        },

        updatePV(){
                this.removePV();
                this.addPV();
                $.notify({message: 'PV Updated !'},{type: 'info'});
        },

        checkExists(){
            this.exists=false;
            let nodeID=this.selectedNode;
            for (let i=0; i<this.value.length; i++){
                    if (this.value[i].node_id===nodeID){
                        this.exists=true;
                    }
                }     
        },
    },
    watch: {
        modelName(val) {
            this.redraw();
        }
    },

    template: `<div style="display: none;">
        <div ref="popup">
            <div class="form-group" v-if="this.exists===false">
                Add PV with Power (kW):
                <input v-model:value.number="power" type="number" step="any" class="form-control form-control-sm" style="width: 100px" placeholder="Power" aria-label="Power">
            </div>
            <button  v-if="this.exists===false" type="button"  class="btn btn-primary btn-sm" @click="addPV" > Add PV </button>
            <div class="form-group" v-if="this.exists===true">
                Update PV Power (kW):
                <input v-model:value.number="power" type="number" step="any" class="form-control form-control-sm" style="width: 100px" placeholder="Power" aria-label="Power">
            </div>
            <button v-if="this.exists===true" type="button"  class="btn btn-primary btn-sm" @click="updatePV" > Update PV </button>
            <button v-if="this.exists===true" type="button"  class="btn btn-secondary btn-sm" @click="removePV" > Remove PV </button>
        </div>
    </div>`
}

export const AddLoadLayer = {
    mixins: [Layer],
    props: {
        modelName: null,
        value: { required: true, default() { return [];}, }, 
    },
    data(){
        return {
            selectedNode: null,
            power: null,
            currentMarker: null,
            exists: null,
        }
    },
    methods: {
        async getLayer() {
            let geojson = await CyderAPI.rest('GET', `/api/models/${encodeURI(this.modelName)}/geojson/`);
            let pointToLayer = (feature, latlng) => {
                var circle = L.circle(latlng, {
                    color: 'red',
                    weight: 2,
                    fillOpacity: 1,
                    radius: 5
                });
                circle.bindPopup(this.$refs.popup);
                circle.on("click", () => this.selectedNode=feature.properties.id);
                circle.on("click", () => this.currentMarker=circle);
                circle.on("click", () => this.checkExists());

                for (let i=0; i<this.value.length; i++){
                    if (this.value[i].node_id===feature.properties.id){
                        circle.setStyle({color: '#14e54c'});
                    }
                }

                return circle;
                }
            return L.geoJson(geojson, {
                pointToLayer,
                //onEachFeature
            });
        },

        addLoad(){
            if (this.power!=null){
                let valueObject= { 
                        node_id: this.selectedNode,
                        power: this.power, 
                    };
                this.value.push(valueObject);
                this.currentMarker.setStyle({color: '#14e54c'});
            }
            this.checkExists();
            $.notify({message: 'Load Added !'},{type: 'success'});

        },
        removeLoad(){
                let nodeID=this.selectedNode;
                for (let i=0; i<this.value.length; i++){
                    if (this.value[i].node_id===nodeID){
                        this.value.splice(i, 1);
                    }
                }
                this.currentMarker.setStyle({color: 'red'});
                 this.checkExists();
                $.notify({message: 'Load Removed !'},{type: 'warning'});
        },

        updateLoad(){
                this.removeLoad();
                this.addLoad();
                $.notify({message: 'Load Updated !'},{type: 'info'});
        },

        checkExists(){
            this.exists=false;
            let nodeID=this.selectedNode;
            for (let i=0; i<this.value.length; i++){
                    if (this.value[i].node_id===nodeID){
                        this.exists=true;
                    }
                }
        },
    },
    watch: {
        modelName(val) {
            this.redraw();
        }
    },

    template: `<div style="display: none;">
        <div ref="popup">
            <div class="form-group" v-if="this.exists===false">
                Add Load with Power (kW):
                <input v-model:value.number="power" type="number" step="any" class="form-control form-control-sm" style="width: 100px" placeholder="Power" aria-label="Power">
            </div>
            <button  v-if="this.exists===false" type="button"  class="btn btn-primary btn-sm" @click="addLoad" > Add Load </button>
            <div class="form-group" v-if="this.exists===true">
                Update Load Power (kW):
                <input v-model:value.number="power" type="number" step="any" class="form-control form-control-sm" style="width: 100px" placeholder="Power" aria-label="Power">
            </div>
            <button v-if="this.exists===true" type="button"  class="btn btn-primary btn-sm" @click="updateLoad" > Update Load </button>
            <button v-if="this.exists===true" type="button"  class="btn btn-secondary btn-sm" @click="removeLoad" > Remove Load </button>
        </div>
    </div>`
}
