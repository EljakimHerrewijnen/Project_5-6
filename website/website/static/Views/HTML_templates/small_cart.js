function SmallCart() {
    var self = this;
    var boo = true;
    this.Cart = {"products": []};

    this.updateCart = function (cb){
        var cart = JSON.parse(localStorage.getItem("shoppingCart"));
        if (!cart) {
            return;
        }
        if(cart.length > 0) {
            $('#small-cart').addClass("visible");
        } else {
            $('#small-cart').removeClass("visible");
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
            smallCart.Cart = cartcontents;
            if(boo) {
                setupContent();
                boo = false;
            }
            updateContent(cb);
        });
    };

    function setupContent() {
        ajaxCall("/static/Views/HTML_templates/small_cart.html", "text", {}, function(_view) {
            $("#cart-content").html("");
            var view = Handlebars.compile(_view);
            $("#view-container").append(view(smallCart.Cart));
            updateLocalStorageCart();
        }); 
    }

    function updateContent(cb) {
        ajaxCall("/static/Views/HTML_templates/cart_row.html", "text", {}, function(_view) {
            $("#cart-content").html("");
            var view = Handlebars.compile(_view);
            $("#cart-content").append(view(smallCart.Cart));
            hideInstant();
            updateLocalStorageCart();
            if(cb)
                cb();
        });   
    }

    function updateLocalStorageCart() {
        var cart = smallCart.Cart.products.map(function(x) {
            return {"id" : x.product_id, "amount": x.amount}
        });
        localStorage.setItem("shoppingCart", JSON.stringify(cart));
    }

    this.increment = function(id) {
        var i = smallCart.Cart.products.find(function(x){
            return x.product_id == id;
        })
        i.amount = i.amount + 1;
        $("#cart-row-amount-" + id).html(i.amount);
        $("#cart-row-price-" + id).html("€" + (i.amount * i.price).toFixed(2));
        updateLocalStorageCart();
    }

    this.decrement = function(id) {
        var i = smallCart.Cart.products.find(function(x){
            return x.product_id == id;
        })
        i.amount = i.amount - 1;
        $("#cart-row-amount-" + id).html(i.amount);
        $("#cart-row-price-" + id).html("€" + (i.amount * i.price).toFixed(2));
        updateLocalStorageCart();
    }

}

var smallCart;

function increment(id) {
    smallCart.increment(id);
}

function decrement(id) {
    smallCart.decrement(id);
}

$('document').ready(function(x) {
    smallCart = new SmallCart();
    smallCart.updateCart(function() {
        $("#small-cart").css("bottom", getSmallCartHiddenPosition());
        $("#small-cart").hover(onHoverSmallCart, onStopHoverSmallCart);
    });
});  

function smallCartChange() {
    smallCart.updateCart(updateCartPosition);
}

function updateCartPosition() {
    var e = $("#small-cart");
    $("#small-cart").hover(onHoverSmallCart, onStopHoverSmallCart);
    if (JSON.parse(localStorage.getItem("shoppingCart")).length > 0) {
        popUpSmallCart();
    } else {
        smallCartHide();
    }
}

function popUpSmallCart() {
    var e = $("#small-cart");
    var h = e.height();
    e.animate({
        "bottom" : 0
    }, 200).delay(1000).animate({
        "bottom" : getSmallCartHiddenPosition()
    }, 200);
}

function hideInstant() {
    $("#small-cart").css("bottom", getSmallCartHiddenPosition());
}

function smallCartHide() {
    $("#small-cart").animate({
        "bottom" : getSmallCartHiddenPosition()
    });
}

function onHoverSmallCart() {
    var e = $("#small-cart");
    e.stop(true);
    e.animate({
        "bottom" : 0
    }, 200);
}

function onStopHoverSmallCart() {
    var e = $("#small-cart");
    e.stop(true);
    e.animate({
        "bottom" : getSmallCartHiddenPosition()
    }, 200)
}

function getSmallCartHiddenPosition() {
    var e = $("#small-cart");
    if (JSON.parse(localStorage.getItem("shoppingCart")).length > 0) {
        return -e.height() + 38
    } else {
        return -e.height() - 5
    }
}