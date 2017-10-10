(function() {

window.viewlib = {};

viewlib.View = class View {
    constructor() {
        this._isbuilt = false;
        this._parentFrame = null;
    }
    get parentView() {
        if(this._parentFrame) return this._parentFrame.parentView;
        else return null;
    }
    get isbuild() { return this._isbuilt; }
    get isshown() { return this._parentFrame && this._parentFrame.isshow; }

    // Following functions can be override
    _onbuild(done) { done(); }
    _onshow(done) { done(); }
    _onhide(done) { done(); }
    _onactivate(done) { done(); }
    _ondeactivate(done) { done(); }

    // Following functions must only be callel by ViewFrame (see this as a kind of c++ like friendship)
    _build() {
        return new Promise(resolve => this._onbuild(resolve))
        .then(() => { this._isbuilt = true; });
    }
    _show() {
        return new Promise(resolve => this._onshow(resolve));
    }
    _hide() {
        return new Promise(resolve => this._onhide(resolve));
    }
    _activate(parentFrame) {
        if(this._parentFrame)
            throw `This view (${this.constructor.name}) is already in a frame. A view can't be in more than one frame at a time`;
        this._parentFrame = parentFrame;

        return (() => { // Build the view if needed
            if(this._isbuilt)
                return Promise.resolve();

            return this._build();
        })()
        .then(() => { return new Promise(resolve => this._onactivate(resolve))});
    }
    _deactivate() {
        this._parentFrame = null;
        return new Promise(resolve => this._ondeactivate(resolve));
    }
}

viewlib.ViewFrame = class ViewFrame {
    constructor(parentView = null) {
        this._currentView = null;
        this._isshown = true;
        this._parentView = parentView;
    }
    get currentView() { return this._currentView; }
    get parentView() { return this._parentView; }
    get isshown() { return this._isshown; }

    changeView(view) {
        if(view == this._currentView)
            return Promise.resolve();

        return (() => { // Hide and deactivate the current view if needed
            if(!this._currentView)
                return Promise.resolve();

            return (() => { // Hide the current view if needed
                if(!this._isshown)
                    return Promise.resolve();
                return this._currentView._hide();
            })()
            .then(() => { return this._currentView._deactivate(); });
        })()
        .then(() => { this._currentView = view; })
        .then(() => { // Activate and show the new view if needed
            if(!this._currentView)
                return Promise.resolve();

            return this._currentView._activate(this)
            .then(() => { // Show the new view if needed
                if(!this._isshown)
                    return Promise.resolve();
                return this._currentView._show();
            });
        });
    }
    show() {
        this._isshown = true;
        if(this._currentView)
            return this._currentView._show();
        else
            return Promise.resolve();
    }
    hide() {
        this._isshown = false;
        if(this._currentView)
            return this._currentView._hide();
        else
            return Promise.resolve();
    }
}

// Test
class TestView extends viewlib.View {
    constructor() { super(); }

    _onbuild(done) { setTimeout(() => { console.log("built!"); done(); }, 1000); }
    _onshow(done) { setTimeout(() => { console.log("shown!"); done(); }, 1000); }
    _onhide(done) { setTimeout(() => { console.log("hidden!"); done(); }, 1000); }
    _onactivate(done) { setTimeout(() => { console.log("activated!"); done(); }, 1000); }
    _ondeactivate(done) { setTimeout(() => { console.log("deactivated!"); done(); }, 1000); }
}
// Each line should appear one second after the precedent (except for the 'end' one)
function test() {
    var viewFrame = new viewlib.ViewFrame();

    var a = new TestView();
    var b = new TestView();

    console.log("start");
    viewFrame.hide().then(() => {
        return viewFrame.changeView(a);
        // built!
        // activated!
    }).then(() => {
        return viewFrame.show();
        // shown!
    }).then(() => {
        return viewFrame.changeView(b);
        // hidden!
        // deactivated!
        // built!
        // activated!
        // shown!
    }).then(() => {
        return viewFrame.hide();
        // hidden!
    }).then(() => {
        return viewFrame.changeView(a);
        // deactivated!
        // activated!
    }).then(() => {
        return viewFrame.show();
        // shown!
    }).then(() => {
        console.log("end");
    });
}
//test();

})();
