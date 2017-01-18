viewManager.addRoute("/admin/dashboard", () => new adminDashboard());

function adminDashboard() {
    var self = this;
    var container;

    Object.defineProperty(this, "url", {
        get : () => '/admin/dashboard'
    });

    this.construct = function(newContainer) {
        container = newContainer;
        var html = getHtml();
        var users = getUsers()

        promise = Promise.all([html, users]).then(([html, users]) =>{
            html = Handlebars.compile(html);
            container.append(html(users));
            container.css({opacity: 0});
        });

        return promise;
    }

    this.destruct = function() {
        return container.animate({opacity:0}, 150).promise().then(() => container.remove());
    }

    this.transitionIn =function() {
        container.animate({opacity: 1}, 150);
    }
    
    var getHtml = () => $.ajax({url: "/static/views/admin/dashboard.html"});
    var getUsers = () => $.ajax({url: "/api/admin/account"});
}