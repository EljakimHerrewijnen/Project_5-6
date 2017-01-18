viewManager.addRoute("/wishlists", () => new browseWishlistView());


function browseWishlistView() {
    var self = this;
    var wishlists;

    Object.defineProperty(this, "url", {
        get : () => '/wishlists'
    });

    this.construct = function(newContainer) {
        container = newContainer;
        var html = getHtml();
        var wishLists = stateManager.getProducts();
        var cart = Cart;

        promise = Promise.all([html, products]).then(([html, products]) =>{
            html = Handlebars.compile(html);
            container.append(html(Cart.items));
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
    
    var getHtml = () => $.ajax({url: "/static/views/cart-view.html",contentType: "text"});
}