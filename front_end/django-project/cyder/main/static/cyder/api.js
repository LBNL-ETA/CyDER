(function() {
    window.CyderAPI = {};

    let token;
    CyderAPI.auth = function(username = null, password=null) {
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
                    reject(xhr);
                }
            };

            if(username && password)
                xhr.send({ username, password });
            else
                xhr.send();
        });
        return token;
    };

    CyderAPI.rest = function(method, url, content, contentType) {
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
                    reject(new CyderAPI.Error(xhr));
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

    /* Deprecated */ CyderAPI.smartRest = async function(...args) {
        try {
            return await CyderAPI.rest(...args);
        } catch(e) {
            if(e instanceof CyderAPI.Error)
                e.notify();
            throw e;
        }
    };

    CyderAPI.Error = class extends Error {
        constructor(xhr) {
            super();
            this.xhr = xhr;
            this.name = 'CyderAPI Error';
            this.notify();
        }
        get message() {
            switch(this.xhr.status) {
            case 400:
                let msg = '';
                for(let field in this.xhr.response) {
                    msg += '${field}\n'
                    for(let hint of this.xhr.response[field])
                        msg += '    \n${hint}';
                }
                return msg;
                break;
            default:
                return `${this.xhr.statusText}(${this.xhr.response.detail})`;
                break;
            }
        }
        notify() {
            switch(this.xhr.status) {
            case 400:
                for(let field in this.xhr.response) {
                    let msg = '';
                    for(let hint of this.xhr.response[field])
                        msg += '<br>' + hint;
                    $.notify({title: `<strong>${field}:</strong>`, message: msg},{type: 'danger'});
                }
                break;
            case 500:
                $.notify({title: `<strong>The server is in trouble :'(</strong><br>`, message: `It sounds really bad but some really devoted<br>people are working hard on it !`},{type: 'danger'});
                break;
            default:
                $.notify({title: `<strong>${this.xhr.statusText}:</strong>`, message: this.xhr.response.detail},{type: 'danger'});
                break;
            }
        }
    }

    let modelsProm;
    CyderAPI.getModels = function(force = false) {
        if(this.modelsProm && !force)
            return this.modelsProm;
        return this.modelsProm = CyderAPI.rest('GET', '/api/models/');
    };
    CyderAPI.getModelsDict = function(force = false) {
        return CyderAPI.getModels(force).then((models) =>
            models.reduce((obj, model) => {obj[model.name] = model; return obj;}, {})
        );
    };

})();
