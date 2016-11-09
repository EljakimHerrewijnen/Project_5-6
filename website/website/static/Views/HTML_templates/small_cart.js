function SmallCart() {
    var self = this;
    this.html = "<div id='small-cart'><div>Small cart</div><a href='http://localhost:5555/orderview'>Checkout</a></div>";
    this.cart = {"products": []};

    this.updateCart = function (){
        var cart = JSON.parse(localStorage.getItem("shoppingCart"));
        if (!cart) {
            return;
        }
        if(cart.length > 0) {
            $('#small-cart').addClass("visible");
        } else {
            $('#small-cart').removeclass("visible");
        }
        
        cart = cart.map(function(x) {return x['id']});
        ajaxCall("/API/Products", "application/json", {}, function(json){
            var shop = JSON.parse(localStorage.getItem("shoppingCart"));
            json = json.map(function(x) { x["price"] = x["price"].toFixed(2); return x;})
            var cartcontents = {}
            cartcontents["products"] = json.filter(function(x) {
                return cart.includes(x.product_id);
            });

            cartcontents.products.forEach(function(x) {
                var i = cart.indexOf(x.product_id);
                if (i != -1) {
                    x["amount"] = shop[i]["amount"]
                }
            });
            this.cart = cartcontents;
            console.log(this.cart);
            updateContent();
        });
    };

    function updateContent() {
        ajaxCall("/static/Views/HTML_templates/small_cart.html", "text", {}, function(_view) {
            $("#cart-content").html("");
            var view = Handlebars.compile(_view);
            $("#view-container").append(view(this.cart));
        });   
    }

}

$('document').ready(function(x) {
    var smallCart = new SmallCart();
    smallCart.updateCart();
});  