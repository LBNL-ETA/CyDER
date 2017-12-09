'use strict';

let token;
function auth(username = null, password=null) {
    token = new Promise(function(resolve, reject) {
        var xhr = new XMLHttpRequest();

        if(username && password)
            xhr.open('POST', '/api/token-auth/', true);
        else
            xhr.open('GET', '/api/token-session/', true);

        xhr.responseType = 'json';
        xhr.onload = function() {
            if (xhr.status === 200) {
                token = xhr.response.token;
                resolve();
            } else {
                reject(new RESTError(xhr));
            }
        };

        if(username && password)
            xhr.send({ username, password });
        else
            xhr.send();
    });
    return token;
};

function rest(method, url, content, contentType) {
    return new Promise(async function(resolve, reject) {
        if(!token)
            throw new Error("CyderAPI.auth() have to be call first to use the API");
        if(token instanceof Promise)
            await token;

        var xhr = new XMLHttpRequest();
        xhr.open(method, url, true);
        xhr.responseType = 'json';
        xhr.setRequestHeader('Authorization', `Token ${ token }`);
        xhr.onload = function() {
            if (xhr.status >= 200 && xhr.status < 300) {
                resolve(xhr.response);
            } else {
                reject(new RESTError(xhr));
            }
        };
        if(contentType) {
            xhr.setRequestHeader('Content-type', contentType);
            xhr.send(content);
        }
        else if(content) {
            xhr.setRequestHeader('Content-type', 'application/json');
            xhr.send(JSON.stringify(content));
        }
        else
            xhr.send();
    });
};

class RESTError extends Error {
    constructor(xhr) {
        super();
        this.xhr = xhr;
        this.name = 'CyDER REST API Error';
    }
    get message() {
        switch(this.xhr.status) {
        case 400:
            let msg = '';
            for(let field in this.xhr.response) {
                msg += `${field}\n`
                for(let hint of this.xhr.response[field])
                    msg += `    \n${hint}`;
            }
            return msg;
            break;
        default:
            return `${this.xhr.statusText}(${this.xhr.response.detail})`;
            break;
        }
    }
}

class Res {
    constructor(url, lookup) {
        this._url = url;
        this._lookup = lookup;

        this._areAllLoaded = false;
        this._res = new Map();
        this._resProm = new Map();
    }
    _getLookupUrl(lookup) {
        return `${this._url}${encodeURI(lookup)}/`;
    }
    getAll(force = false) {
        if(this._areAllLoaded === true && !force)
            return this._res;
        if(!(this._resProm instanceof Promise)) {
            this._resProm = rest('GET', this._url).then((resArray) => {
                this._areAllLoaded = true;
                this._resProm = new Map();
                return this._res = new Map(resArray.map((res) => [res[this._lookup], res]));
                });
        }
        return this._resProm;
    }
    get(lookup, force = false) {
        let res = this._res.get(lookup);
        if(res && !force)
            return res;
        if(this._resProm instanceof Promise)
            return this._resProm.then((resMap) => resMap.get(lookup));
        if(!(this._resProm.get(lookup) instanceof Promise)) {
            this._resProm.set(lookup, rest('GET', this._getLookupUrl(lookup)).then((res) => {
                this._resProm.delete(lookup);
                this._res.set(lookup, res)
                return res;
            }));
        }
        return this._resProm.get(lookup);
    }
};
Res.WriteMixin = (superclass) => class extends superclass {
    async create(res) {
        let newRes = await rest('POST', this._url, res);
        this._res.set(newRes[this._lookup], newRes)
        return newRes;
    }
    async update(lookup, res) {
        let newRes = await rest('PATCH', this._getLookupUrl(lookup), res);
        this._res.set(lookup, newRes)
        return newRes;
    }
};
Res.DeleteMixin = (superclass) => class extends superclass {
    async delete(lookup) {
        await rest('DELETE', this._getLookupUrl(lookup));
        this._res.delete(lookup);
    }
};
class NestedRes {
    constructor(parent, subURL, lookup, ResClass = Res) {
        this._parent = parent; // Instance of Res or NestedRes
        if(this._parent instanceof Res)
            this._depth = 1;
        else if(this._parent instanceof NestedRes)
            this._depth = this._parent._depth + 1;
        this._subURL = subURL;
        this._lookup = lookup;
        this._ResClass = ResClass;

        this._nestedRes = new Map();
        return new Proxy(this, NestedRes.handler);
    }
    _getResObject(...args) {
        let url = this._parent._getLookupUrl(...args);
        let nestedRes = this._nestedRes.get(url);
        if(!nestedRes) {
            nestedRes = new this._ResClass(url + this._subURL, this._lookup);
            this._nestedRes.set(url, nestedRes);
        }
        return nestedRes;
    }
    _getLookupUrl(...args) {
        let lookup = args.pop();
        return `${this._parent._getLookupUrl(...args)}${this._subURL}${encodeURI(lookup)}/`;
    }
}
NestedRes.handler = {
    get: function(target, prop) {
        if(prop[0] === '_')
            return target[prop];
        return function(...args) {
            let nestedResArgs = args.slice(0, target._depth)
            let targetArgs = args.slice(target._depth);
            return target._getResObject(...nestedResArgs)[prop](...targetArgs);
        };
    },
    getPrototypeOf: target => NestedRes.prototype,
};

class ProjectRes extends Res.DeleteMixin(Res.WriteMixin(Res)) {
    runConfig(lookup) {
        return rest('POST', `${this._getLookupUrl(lookup)}run_config/`);
    }
    runSim(lookup) {
        return rest('POST', `${this._getLookupUrl(lookup)}run_sim/`);
    }
    revoke(lookup) {
        return rest('POST', `${this._getLookupUrl(lookup)}revoke/`);
    }
}

let Model = new Res('/api/models/', 'name');
let Node = new NestedRes(Model, 'nodes/', 'node_id');
let Device = new NestedRes(Model, 'devices/', 'device_number');
let Load = new NestedRes(Model, 'loads/', 'device_number');
let Project = new ProjectRes('/api/projects/', 'id');

export { auth, rest, RESTError, Model, Device, Load, Project };
let CyderAPI = { auth, rest, RESTError, Model, Device, Load, Project };
export default CyderAPI;
