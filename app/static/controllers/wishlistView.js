viewManager.addRoute("/wishlist/[\\D\\d]+", (path) => {
    var username = path.split('/').pop();
    return new wishlistView(username);
});

function wishlistView(username) {
    var self = this;
    var container;
    var wishlist;

    Object.defineProperty(this, "url", {
        get : () => '/wishlist/' + username
    });

    this.construct = function(newContainer) {
        container = newContainer;
        var html = getHtml();
        var wishlist = getWishlist(username);

        promise = Promise.all([html, wishlist]).then(([html, wishlist]) =>{
            html = Handlebars.compile(html);
            wishlist['wishlist'] = wishlist['wishlist'].map((x) => new Product(x));

            container.append(html(wishlist));
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
    
    var getHtml = () => $.ajax({url: "/static/views/wishlist-view.html",contentType: "text"});
    var getWishlist = (username) => $.ajax({url: "/api/wishlist/" + username,contentType: "text"});
}