'use strict';
import { LeafletMap } from '../models/viewer-legacy.js';
import { Layer, createPVLayer, createLoadLayer } from '../models/layers.js';
import { View, FOREACH, IF, ESCHTML } from '../viewlib.js';
import CyderAPI from '../api.js';
import notifyRESTError from '../api-notify-error.js';


export const FeederSelector = {
    props:{ 
        feeders : null,
    },
    data (){
        return {
            selected: [],
        }
    },
    methods:{
        parseTimestamp(t){
        },
    },
    watch: {
        selected : function(newSelected, oldSelected){
            //"$emit" captured by "v-on" in parent (child component to parent communication) to update parent SelectedFeeders data dynamically
            this.$emit('selection',this.selected);
        }
    },
    template : `
        <div v-if="this.feeders!=null">
            Select Feeders to edit: 
            <select class="form-control" v-model="selected" multiple >
               <option v-for="f in Object.keys(feeders)" >{{ f }}</option>
            </select>
        </div>
    `
    }

export const FeederViewer = {
    mixins: [Layer],
    props:{ 
        modelName: null,
        selectedFeeders : null,
        feeders: null,
    },
    data (){
        return {
            test: null,
        }
    },
    methods:{
        async getLayer() {
            let geojson = {
                'features' : [],
                'type': 'FeatureCollection'
            }
            for (let i=0; i<this.selectedFeeders.length; i++){
                geojson.features=geojson.features.concat(this.feeders[ this.selectedFeeders[i] ]);
            }
            this.test=geojson;
            let pointToLayer = (feature, latlng) => {
                var circle = L.circle(latlng, {
                    color: 'red',
                    weight: 2,
                    fillOpacity: 1,
                    radius: 5
                });

                return circle;
                }
            return L.geoJson(geojson, {
                pointToLayer,
                //onEachFeature
            });
        },
    },
}