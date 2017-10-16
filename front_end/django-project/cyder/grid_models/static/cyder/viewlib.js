class View {
    constructor(tag, parent = null) {
        this._html = {};
        this._html.el = document.createElement(tag);
        this._childs = {};
        this._parent = parent;
    }
    get el() { return this._html.el; }
    child(name) { return this._childs[name]; }
    get parent() { return this._parent; }
    get _template() { return ''; }
    render() {
        this._html.el.innerHTML = this._template;

        for(let el of this._html.el.querySelectorAll('[data-name]'))
            this._html[el.getAttribute('data-name')] = el;

        for(let el of this._html.el.querySelectorAll('[data-on]')) {
            for(let listner of el.getAttribute('data-on').split(';')) {
                let evt, method;
                [evt, method] = el.getAttribute('data-on').split(':');
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

function FOREACH(array, func) {
    if (array instanceof Array)
        return array.map(func).join('');
    else {
        let res = '';
        for (let key in array)
            res += func(key, array[key]);
        return res;
    }
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
