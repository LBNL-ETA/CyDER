class View {
    constructor(el, tag = 'div') {
        this._html = {};
        if(el)
            this._html.el = el;
        else
            this._html.el = document.createElement(tag);
        this._childs = {};
    }
    get el() { return this._html.el; }
    child(name) { return this._childs[name]; }
    get _template() { return ''; }
    render() {
        this._html.el.innerHTML = this._template;

        for(let el of this._html.el.querySelectorAll('[data-name]'))
            this._html[el.getAttribute('data-name')] = el;

        for(let el of this._html.el.querySelectorAll('[data-on]')) {
            for(let listner of el.getAttribute('data-on').split(';')) {
                let evt, method;
                [evt, method] = el.getAttribute('data-on').split(':');
                if(!(this[method] instanceof Function))
                    throw new Error(`${this.constructor.name} have no method called ${method}
                        Check your data-on arguments`);
                el.addEventListener(evt, (...args) => this[method](...args));
            }
        }

        for(let el of this._html.el.querySelectorAll('[data-childview]'))
            this._childs[el.getAttribute('data-childview')].emplace(el);
    }
    emplace(el) {
        for (let i = 0; i < el.attributes.length; i++) {
            let attr = el.attributes[i];
            if (attr.name === 'style') {
                for(let i = 0; i < el.style.length; i++) {
                    let cssProp = el.style[i];
                    this._html.el.style[cssProp] = el.style[cssProp];
                }
                continue;
            }
            this._html.el.setAttribute(attr.name, attr.value);
        }
        el.parentNode.replaceChild(this._html.el, el);
    }
}

function FOREACH(object, func) {
    if(object instanceof Array)
        return object.map(func).join('');
    if (typeof object[Symbol.iterator] === 'function') {
        let result = '';
        for (let obj of object)
            result += func(obj);
        return result;
    }

    let result = '';
    for (let key in object)
        result += func(key, object[key]);
    return result;
}
function IF(cond, ifTemplate, elseTemplate) {
    if (cond)
        return ifTemplate();
    else {
        if (elseTemplate)
            return elseTemplate();
        else
            return '';
    }
}
