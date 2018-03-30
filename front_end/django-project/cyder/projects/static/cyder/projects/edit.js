'use strict';
import { LeafletMap } from '../models/viewer-legacy.js';
import { Layer, createPVLayer, createLoadLayer } from '../models/layers.js';
import { View, FOREACH, IF, ESCHTML } from '../viewlib.js';
import CyderAPI from '../api.js';
import notifyRESTError from '../api-notify-error.js';

//Responsible for map layer displaying only the selected feeders for the project
export const ProjectModelViewer = {
    mixins: [Layer],
    props:{ 
        modelName: null,
        geojson: null,
    },
    methods:{
        async getLayer() {
            let pointToLayer = (feature, latlng) => {
                var circle = L.circle(latlng, {
                    color: 'red',
                    weight: 2,
                    fillOpacity: 1,
                    radius: 5
                });

                return circle;
                }
            return L.geoJson(this.geojson, {
                pointToLayer,
            });
        },
    },
}

//Responsible for map layer implemeting PV adding funtionalities
export const AddPvLayer = {
    mixins: [Layer],
    props: {
        modelName: null,
        value: { required: true, default() { return [];}, }, 
        geojson: null,
    },
    data(){
        return {
            selectedNode: null,
            selectedFeeder:null,
            power: null,
            exists: null, //boolean indicating whether PV has been added to the selected node yet or not
        }
    },
    methods: {
        async getLayer() {
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

                //Colors in green all nodes where PV has already been added in previous editions of the project
                for (let i=0; i<this.value.length; i++){
                    if (this.value[i].node_id===feature.properties.id){
                        circle.setStyle({color: '#14e54c'});
                    }
                }

                return circle;
                }
            return L.geoJson(this.geojson, {
                pointToLayer,
            });
        },

        addPV(){
        // saves all necessary info for simulation (node id, feeder id and power) to the project settings and colors the node to green indicating that a load has been added
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
        // removes PV info from the project settings and colors the node to back to red indicating that the PV has been removed
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

//Responsible for map layer implemeting Load addition funtionalities, exactly the same implementation as the addPV layer
export const AddLoadLayer = {
    mixins: [Layer],
    props: {
        modelName: null,
        value: { required: true, default() { return [];}, }, 
        geojson: null,
    },
    data(){
        return {
            selectedNode: null,
            selectedFeeder:null,
            power: null,
            exists: null, //boolean indicating whether PV has been added to the selected node yet or not
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
                circle.on("click", () => this.selectedFeeder=feature.properties.feeder);
                circle.on("click", () => this.currentMarker=circle);
                circle.on("click", () => this.checkExists());

                //Colors in green all nodes where PV has already been added in previous editions of the project
                for (let i=0; i<this.value.length; i++){
                    if (this.value[i].node_id===feature.properties.id){
                        circle.setStyle({color: '#14e54c'});
                    }
                }

                return circle;
                }
            return L.geoJson(geojson, {
                pointToLayer,
            });
        },

        addLoad(){
        // saves all necessary info for simulation (node id, feeder id and power) to the project settings and colors the node to green indicating that a load has been added
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
            $.notify({message: 'Load Added !'},{type: 'success'});

        },
        removeLoad(){
        // removes load info from the project settings and colors the node to back to red indicating that the load has been removed
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
