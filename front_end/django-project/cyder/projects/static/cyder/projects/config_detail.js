'use strict';
import CyderAPI from '../api.js';
import notifyRESTError from '../api-notify-error.js';

export const TimestampSelector = {
    props:{ 
        datetimes: null,
    },
    data (){
        return {
            ParsedTimestamp: '',
        }
    },
    methods:{
        parseTimestamp(t){
        return moment(t, "YYYY_MM_DD_HH_mm_ss").toDate().toString();
        },
    },
    watch: {
        ParsedTimestamp : function(newTimestamp, oldTimestamp){
            this.$emit('timestampchanged',moment(this.ParsedTimestamp).format("YYYY_MM_DD_HH_mm_ss"));
        }
    },
    template : `
        <select class="form-control form-control-lg" v-model="ParsedTimestamp">
            <option v-for="t in datetimes" >{{ parseTimestamp(t) }}</option>
        </select>
    `
}