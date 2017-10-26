(function() {
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
                    resolve(token);
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
    }

    function rest(method, url, content, contentType) {
        return new Promise(async function(resolve, reject) {
            if(!token)
                throw "auth() have to be call first to use the API";
            if(token instanceof Promise)
                await token;

            var xhr = new XMLHttpRequest();
            xhr.open(method, url, true);
            xhr.responseType = 'json';
            xhr.setRequestHeader('Authorization', `Token ${ token }`);
            xhr.onload = function() {
                if (xhr.status === 200) {
                    resolve(xhr.response);
                } else {
                    reject(xhr);
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
    }

    window.CyderAPI = {
        auth,
        rest
    };
})();
