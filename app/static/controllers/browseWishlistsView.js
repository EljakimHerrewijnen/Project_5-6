viewManager.addRoute("/wishlists", () => new browseWishlistView());

function browseWishlistView() {
    var self = this;
    var container;
    var wishlists;

    Object.defineProperty(this, "url", {
        get : () => '/wishlists'
    });

    this.construct = function(newContainer) {
        container = newContainer;
        var html = getHtml();
        var wishlists = getWishlists();

        promise = Promise.all([html, wishlists]).then(([html, wishlists]) =>{
            html = Handlebars.compile(html);
            container.append(html(wishlists));
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
    
    var getHtml = () => $.ajax({url: "/static/views/browse-wishlists-view.html",contentType: "text"});
    var getWishlists = () => $.ajax({url: "/api/wishlist" ,contentType: "text"});
}