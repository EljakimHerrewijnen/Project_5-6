var notFoundView = (() => {
    function singleton() {
        var self = this;
        var getHtml = function() {
            return $.ajax({
                url: "http://localhost:5555" + "/static/Views/404/404.html",
                contentType: "text"
            });
        }

        this.construct = function(container) {
            html = getHtml();
            html.then((html) => {
                container.append(html)
            }, (failure) => {
                container.append("error in 404 page");
            });
            return html;
        }

        this.destruct = function(container) {
            return Promise.resolve("no_404");
        }
    }
    return new singleton();
})();

