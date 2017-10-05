(function() {

window.viewlib = {};

viewlib.View = class View {
    constructor(viewSet) {
        if(this.constructor.name == "View") throw "View is an abstract class";
        //this._viewSet = viewSet;
        this._isbuilt = false;
    }

    build() {
        return new Promise(resolve => this._onbuild(resolve))
        .then(() => { this._isbuilt = true;});
    }
    show() {
        return Promise.resolve((() => {
            if(!this._isbuilt)
                return this.build();
        })()).then(() => {
            return new Promise(resolve => this._onshow(resolve));
        });
    }
    hide() {
        return new Promise(resolve => this._onhide(resolve));
    }
}

viewlib.ViewSet = class ViewSet {
    constructor() {
        this._currentView = null;
        this._isshown = true;
    }
    get currentView() { return this._currentView; }

    changeView(view) {
        return Promise.resolve((() => {
            if(this._isshown && this._currentView)
                return this._currentView.hide();
        })()).then(() => {
            this._currentView = view;
            if(this._isshown && this._currentView)
                return this._currentView.show();
        });
    }
    show() {
        this._isshown = true;
        if(this._currentView)
            return this._currentView.show();
        else
            return Promise.resolve();
    }
    hide() {
        this._isshown = false;
        if(this._currentView)
            return this._currentView.hide();
        else
            return Promise.resolve();
    }
}

})();
