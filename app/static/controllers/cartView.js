viewManager.addRoute("/cart", () => new cartView());

function cartView() {
    var self = this;
    var container;

    Object.defineProperty(this, "url", {
        get : () => '/cart'
    });

    this.construct = function(newContainer) {
        container = newContainer;
        cart = stateManager.cart;
        var html = getHtml();
        var products = stateManager.getProducts();
        var cart = Cart;

        promise = Promise.all([html, products]).then(([html, products]) =>{
            html = Handlebars.compile(html);
            container.append(html(Cart.items));
            container.css({opacity: 0});
            if (!cart.isEmpty){
                container.find('#goToOrderButton').removeClass('hidden');
            }
            
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

function _CartUpdateTotal() {
    $("#totalprice").html("€" + Cart.getTotalPrice());
}


Handlebars.registerHelper("cartLineTotal", function(price, amount) {
    return price * amount
});

Handlebars.registerHelper("cartOrderTotal", function() {
    return Cart.getTotalPrice();
})

function _cartIncrement(id) {
    var item = Cart.getItem(id);
    Cart.addProduct(item.product);
    _CartUpdateTotal();
    $("#cart-row-amount-" + id).html(item.quantity);
    $("#cart-row-price-" + id).html("€" + Cart.getItemPrice(id));
}

function _cartDecrement(id) {
    var item = Cart.getItem(id);
    Cart.increment(id, -1);
    if (item.quantity < 1){
        _cartRemoveItem(id);
        return;
    }
    _CartUpdateTotal();
    $("#cart-row-amount-" + id).html(item.quantity);
    $("#cart-row-price-" + id).html("€" + Cart.getItemPrice(id));
}

function _cartRemoveItem(id) {
    Cart.removeProduct(id);
    $("#cart-row-amount-" + id).closest('tr').remove()
    _CartUpdateTotal();
}