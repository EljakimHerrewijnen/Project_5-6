var ViewManager = (function() {
    function ViewManager() {
        var self = this;
        var activeView = undefined;
        var routes = []
        this.container = $('#view-container')

        Object.defineProperty(this, "activeView", {
            get : () => activeView
        });

        this.addRoute = function(pathAsRegex, routeFunction) {
            var re = new RegExp(pathAsRegex + "$");
            if (re in routes) throw new Error("Could not add route, there already exists a route with this path");
            routes.push({
                regExp: re,
                route: routeFunction
            });
        }

        this.redirect = function(path, trackHistory) {
            var route = routes.reduce((acc, route) => route.regExp.test(path) ? route.route : acc, undefined);
            if (route)
                this.changeView(route(path), trackHistory)
            else if (!DEBUG)
                window.location = "http://" + window.location.host + "/404";
            else {
                console.log("Route does not exist")
            }
        }

        this.changeView = function(newActiveView, ignoreHistory) {
            if (newActiveView == activeView) return;
            var newContainer = $('<div></div>');
            MobileMenuBar.hide();
            newActiveView.construct(newContainer)
            .catch((jqXHR) => {
                console.log(jqXHR);
                if (jqXHR.status == 401) {
                    if (activeView == loginRegisterView) return Promise.reject();
                    newActiveView = loginRegisterView;   
                }
                else {
                    //window.location = "http://" + window.location.host + "/404";
                }
                return newActiveView.construct(newContainer);
            }).then(() => {
                if (activeView) {
                    return activeView.destruct();
                }
                else {
                    return Promise.resolve();
                }  
            }).then(() => {
                activeView = newActiveView;
                if (!ignoreHistory) {
                    history.pushState({path: activeView.url}, "", activeView.url);
                }
                self.container.append(newContainer);
                activeView.transitionIn();
                Snackbar.update();
                setupTextfields();
            }).catch((e) => {
                console.log(e)
                console.log(e.responseText)
            });
        }

        window.onpopstate = function(event) {
            self.redirect(event.state.path, true);
        }
    }
    return new ViewManager()
})();

viewManager = ViewManager;

$(document).ready(() => {
    var path = window.location.pathname;
    viewManager.redirect(path);
});

