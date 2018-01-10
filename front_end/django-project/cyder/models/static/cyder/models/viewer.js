'use strict';
import CyderAPI from '../api.js';

export const ModelSelector = {
    model: { prop: 'value', event: 'change' },
    props: {
        allowEmpty: Boolean,
        value: String,
        initModels: {
            default() { return (async () => {
                return Array.from((await CyderAPI.Model.getAll()).keys());
            })(); }
        },
    },
    data() { return {
        models: this.initModels,
    };},
    template: `
        <select @change="$emit('change', $event.target.value)" :value="value" class="custom-select" :disabled="isLoading">
            <option v-if="allowEmpty" value=""></option>
            <option v-if="!isLoading" v-for="model in models">{{ model }}</option>
        </select>`,
    computed: {
        isLoading() { return this.models instanceof Promise; },
    },
    watch: {
        models: {
            immediate: true,
            handler(value) {
                if(value instanceof Promise)
                    value.then((models) => { this.models = models; });
            },
        }
    },
    updated() { this.$el.value = this.value; }
};
