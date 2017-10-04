(function() {

var statetype = {};
var currentstate;
var currentstatedata;
function reState(state) {
    var typeclass = statetype[state._type];
    if(typeclass == undefined) {
        console.error(state._type + " is not registered, you may have forgot to call registerStateClass() on one of your state class");
        return null;
    }
    try {
        var stateObj = new typeclass();
    } catch(erre) {
        console.warn("Make sure all your state class can be instanciate with an empty constructor");
    }
    Object.assign(stateObj, state);
    for (var statename in stateObj._substates) {
        stateObj._substates[statename] = reState(stateObj._substates[statename]);
    }
    return stateObj;
}

var statelib = {};
window.statelib = statelib;

statelib.onpopstate = function(e) {
    var state = reState(e.state);
    state.restore();
};
statelib.pushState = function(url) {
    currentstate._type = currentstate.constructor.name;
    history.pushState(currentstate, "", url);
};
statelib.replaceState = function(url) {
    currentstate._type = currentstate.constructor.name;
    history.replaceState(currentstate, "", url);
};
statelib.registerStateClass = function(varclass) {
    statetype[varclass.name] = varclass;
};
statelib.currentstate = function () { return currentstate; }

statelib.GenericState = class {
    constructor(parent = null, name = '') {
        this._type = this.constructor.name;
        this._substates = {};
        this._parentstate = parent;
        this._substatename  = name;
    }

    iscurrentstate() {
        if(this._parentstate == null) {
            return currentstate === this;
        } else {
            return this._parentstate.iscurrentstate() && this._parentstate._substates[this._substatename] === this;
        }
    }
    get data() {
        if(this._parentstate == null)
            return currentstatedata;
        else
            return this._parentstate.data._substates[this._substatename];
    }
    _resetdata() {
        if(this._parentstate == null)
            currentstatedata = { _substates: {} };
        else
            this._parentstate.data._substates[this._substatename] = { _substates: {} };
    }
    get parent() {
        return this._parentstate;
    }
    getsubstate(name) {
        name
        return this._substates[name];
    }
    get type() {
        return this._type;
    }

    restore() {
        if(this._parentstate == null) {
            if(currentstate !== this) {
                if(currentstate) currentstate.abolish();
                this._resetdata();
                currentstate = this;
                this._onrestore();
                for (var statename in this._substates) {
                    this._substates[statename].restore();
                }
            }
        } else {
            if(this._parentstate.iscurrentstate()) {
                var substate = this._parentstate._substates[this._substatename];
                if(substate !== this) {
                    if(substate) substate.abolish();
                    this._parentstate._substates[this._substatename] = this;
                }
                this._resetdata();
                this._onrestore();
                for (var statename in this._substates) {
                    this._substates[statename].restore();
                }
            } else {
                this._parentstate._substates[this._substatename] = this;
                this._parentstate.restore();
            }
        }
    }
    abolish() {
        if(!this.iscurrentstate()) {
            throw "statelib: Can't abolish a state wich is not the current state!";
        }
        for(var statename in this._substates) {
            this._substates[statename].abolish();
        }
        this._onabolish();
        if(this._parentstate == null) {
            currentstate = null;
        } else {
            delete this._parentstate._substates[this._substatename];
        }
    }

    _onrestore() {}
    _onabolish() {}
};
statelib.registerStateClass(statelib.GenericState);

currentstate = null;

})();
