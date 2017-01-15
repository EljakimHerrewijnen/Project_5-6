function ViewController() {
    var self = this;
    var currentView;
    var mainContainer = $("#view-container");

    this.viewContainer = $("<div id='viewContainer'></div>").appendTo(mainContainer);
    this.cartDrawer = new cartDrawer();
    this.urlMarshal = new URLMarshall(self);
    this.storage = {};

    this.changeToView = function* (newView) {
        yield currentView.deconstruct();
        yield newView.construct(self);
        currentView = newView;
    }
}


function URLMarshall(viewController) {
    var self = this;

    function getCurrentPath() {}

    this.getViewForURL = function() {
        return new BaseView(viewController);
    }
}


function BaseView(viewController) {
    this.construct = function* () {
        var html = $("<div></div>");
        viewController.viewContainer.append(html);
    }

    this.deconstruct = function* () {
        ViewController.viewContainer.empty();
    }
}