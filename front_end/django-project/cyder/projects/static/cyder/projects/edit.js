'use strict';
import { LeafletMap } from '../models/viewer-legacy.js';
import { Layer, createPVLayer, createLoadLayer } from '../models/layers.js';
import { View, FOREACH, IF, ESCHTML } from '../viewlib.js';
import CyderAPI from '../api.js';
import notifyRESTError from '../api-notify-error.js';


export const ChangePowerLayer = {
    mixins: [Layer],
    props: {
        modelName: { type: String, required: true },
        deviceType: { type: String, required: true },
        value: { required: true, default() { return [];}, },
    },
    data() { return {
        currentPopup: {
            defaultValue: null,
            valueObject: { device_number: '', power: 0 },
        },
    };},
    methods: {
        getLayer() {
            if(this.deviceType === 'pv') {
                let bindDevicePopup = (pv, device, marker) => {
                    let pvValue = pv.PVActiveGeneration ? pv.PVActiveGeneration : 0;
                    marker.bindPopup(this.$refs.popup);
                    marker.on('click', () => {
                        this.currentPopup.valueObject = this.value.find((el) => el.device_number === device.device_number);
                        if(this.currentPopup.valueObject === undefined)
                            this.currentPopup.valueObject = {
                                device_number: device.device_number,
                                power: 0,
                            };
                        this.currentPopup.defaultValue = pvValue;
                        this.currentPopup.marker = marker;
                    });
                    if(this.value.find((el) => el.device_number === device.device_number))
                        marker.setStyle({color: '#14e54c'});
                };
                return createPVLayer(this.modelName, bindDevicePopup);
            }
            if(this.deviceType === 'load') {
                let bindDevicePopup = (load, device, marker) => {
                    let loadValue = (load.SpotKWA ? load.SpotKWA : 0) + (load.SpotKWB ? load.SpotKWB : 0) + (load.SpotKWC ? load.SpotKWC : 0);
                    marker.bindPopup(this.$refs.popup);
                    marker.on('click', () => {
                        this.currentPopup.valueObject = this.value.find((el) => el.device_number === device.device_number);
                        if(this.currentPopup.valueObject === undefined)
                            this.currentPopup.valueObject = {
                                device_number: device.device_number,
                                power: 0,
                            };
                        this.currentPopup.defaultValue = loadValue;
                        this.currentPopup.marker = marker;
                    });
                    if(this.value.find((el) => el.device_number === device.device_number))
                        marker.setStyle({color: '#14e54c'});
                };
                return createLoadLayer(this.modelName, bindDevicePopup);
            }
        },
        _reset() {
            if(this.currentPopup.valueObject.power === 0)
                return;
            this.currentPopup.valueObject.power = 0;
            this.value.splice(this.value.indexOf(this.currentPopup.valueObject), 1);
            this.currentPopup.marker.setStyle({color: '#3388ff'});
            this.$emit('input', this.value);
        },
        _set(event) {
            let power = Number(event.target.value)-this.currentPopup.defaultValue;
            if(Number.isNaN(power) || event.target.value === "") {
                $.notify({ message: 'Power must be a number'}, {type: 'danger'});
                event.target.value = this.currentPopup.defaultValue+this.currentPopup.valueObject.power;
                return;
            }
            if(power === 0) {
                this._reset();
                return;
            }
            if(this.currentPopup.valueObject.power === 0)
                this.value.push(this.currentPopup.valueObject);
            this.currentPopup.marker.setStyle({color: '#14e54c'});
            this.currentPopup.valueObject.power = power;
            this.$emit('input', this.value);
        },
    },
    template: `<div style="display: none;">
        <div ref="popup">
            <div class="form-group">
                Power (kW):
                <input :value="currentPopup.defaultValue+currentPopup.valueObject.power" @change="_set" type="number" step="any" class="form-control form-control-sm" style="width: 100px" placeholder="Power" aria-label="Power">
            </div>
            <button v-if="currentPopup.valueObject.power!==0" type="button" @click="_reset" class="btn btn-primary btn-sm">Reset</button>
        </div>
    </div>`,
    watch: {
        deviceType() {
            this.redraw();
        }
    }
}

export const AddPvLayer = {
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
                    fillOpacity: 0.5,
                    radius: 5
                });
                circle.bindPopup(this.$refs.popup);
                circle.on("click", () => this.selectedNode=feature.properties.id);
                circle.on("click", () => this.currentMarker=circle);
                circle.on("click", () => this.checkExists());

                for (let i=0; i<this.value.length; i++){
                    if (this.value[i].device_number===feature.properties.id){
                        circle.setStyle({
                            color: '#14e54c',
                            weight: 10,
                            fillOpacity: 0.75,
                            radius: 10,
                        });
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
                        device_number: this.selectedNode,
                        power: this.power, 
                    };
                this.value.push(valueObject);
                this.$emit('added',valueObject);
                this.currentMarker.setStyle({
                        color: '#14e54c',
                        weight: 10,
                        fillOpacity: 0.75,
                        radius: 10,
                    });
            }
            this.checkExists();

        },
        removePV(){
                let nodeID=this.selectedNode;
                for (let i=0; i<this.value.length; i++){
                    if (this.value[i].device_number===nodeID){
                        this.value.splice(i, 1);
                    }
                }
                //this.value.splice(this.value.indexOf(valueObject), 1);
                //this.$emit('added',valueObject);
                this.currentMarker.setStyle({
                        color: 'red',
                        weight: 2,
                        fillOpacity: 0.5,
                        radius: 5
                    });
        },
        checkExists(){
            this.exists=false;
            let nodeID=this.selectedNode;
            for (let i=0; i<this.value.length; i++){
                    if (this.value[i].device_number===nodeID){
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
            <button v-if="this.exists===true" type="button"  class="btn btn-secondary btn-sm" @click="removePV" > Remove PV </button>
        </div>
    </div>`
}
