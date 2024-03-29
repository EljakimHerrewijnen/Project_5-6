// Global variables.
var product;
var viewContainer = $("#view-container");
var pathname = $(location).attr('pathname');
var id = pathname.substring(pathname.lastIndexOf('/') + 1);
var cartcontents;

var path = window.location.pathname;

viewManager.addRoute('/details/\\d+', (path) => {
    var productId = path.split('/').pop();
    return new productDetailView(productId);
});

function productDetailView(productId) {
    var self = this;
    var container;
    var product;

    Object.defineProperty(this, "url", {
       get : () => '/details/' + productId 
    });

    this.construct = function(c) {
        html = this.getHtml();
        products = stateManager.getProducts();
        return Promise.all([html, products]).then(([html, products]) => {
            var view = Handlebars.compile(html);
            container = c;
            container.css({opacity: 0.0})
            product = products.find((product) => {
                return product.id == productId
            });
            var rProducts = []
            for (var i = 0; i < 3; i++) {
                var rProduct = products[Math.floor(Math.random() * products.length)];
                if (rProduct.id == product.id)
                    i--;
                else
                    rProducts.push(rProduct);
            }
            var content = {
                product: product,
                suggestions: rProducts
            }

            container.append(view(content));
        }).then(() => {
            container.find('#add-to-cart-button').on('click', onAddToCartButtonPressed);
            container.find('#wishlist_button').on('click', onWishButtonPressed);
            container.find('#favorites_button').on('click', onFavoritesButtonPressed);
            user = stateManager.getUser().then((user) => {
                if (user.hasWish(product)){
                    container.find('#wishlist_button').html("<i class='material-icons add-to-cart-button'>add_circle_outline</i><span>REMOVE FROM WISHLIST</span>");
                }
                //If user has not bought the product do not display option to add to favorits
                if (user.hasBought(product)){
                    container.find('#favorites_button').css({"display" : "flex"});
                    //if user has favorited the product chance text to remove
                    if (user.hasFavorite(product)){
                        container.find('#favorites_button').html("<i class='material-icons add-to-cart-button'>favorite_border</i><span>REMOVE FROM FAVORITES</span>");
                    }
                }else{
                    // hide element
                    container.find('#favorites_button').css({"display" : "none"});
                }
            });
        });
    }

    this.destruct = function() {
        var vv = container.animate({opacity: 0.0}, 150).promise().then(() => {container.remove()});
        return vv;
    }

    this.transitionIn = function() {
        container.animate({opacity: 1}, 200);
    }

    this.getHtml = () => $.ajax({url: "/static/views/product-details-view.html", contentType: "text"});

    function onWishButtonPressed() {
        user = stateManager.getUser();
        button = container.find('#wishlist_button')
        user.then((user) => {
            if (user.hasWish(product)) {
                return user.removeWish(product).then(() => button.html("<i class='material-icons add-to-cart-button'>add_circle</i><span>ADD PRODUCT TO WISHLIST</span>"));}
            else
                return user.addWish(product).then(() => button.html("<i class='material-icons add-to-cart-button'>add_circle_outline</i><span>REMOVE FROM WISHLIST</span>"));
        }, (jqXHR, textStatus, errorThrown) => {
            if (jqXHR.status == 400){
                alert(jqXHR.responseText);
            }
            else{
                viewManager.changeView(loginRegisterView);
            }
        });
    }

    function onFavoritesButtonPressed() {
        user = stateManager.getUser();
        button = container.find('#favorites_button')
        user.then((user) => {
            if (user.hasFavorite(product)){
                return user.removeFavorite(product).then(() => {button.html("<i class='material-icons add-to-cart-button'>favorite</i><span>ADD PRODUCT TO FAVORITES</span>")});
            }
            else{
                return user.addFavorite(product).then(() => {button.html("<i class='material-icons add-to-cart-button'>favorite_border</i><span>REMOVE FROM FAVORITES</span>")});
            }
        }, (jqXHR, textStatus, errorThrown) => {
            if (jqXHR.status == 400){
                alert(jqXHR.responseText);
            }
            else{
                viewManager.changeView(loginRegisterView);
            }
        });
    }

    function onAddToCartButtonPressed() {
        Cart.addProduct(product);
    }
}




function storedata()
{    
    // var productname = document.getElementById("cartbutton").value;
    cartcontents = cartcontents + productname;
    window.alert(cartcontents)
    //window.alert("hello");    
    localStorage.setItem("name", productname);
    var namestorage = localStorage.getItem("name");
    //window.alert(namestorage);
}

function setupwishlistButton() {
    var button = $('#wishlist_button');
    var user = authenticationService.User();
    
    // If no user, log in.
    if (!user) {
        button.on("click", function(e) {
            window.location.replace("/login");
        });
        return;
    }

    // Set up initial state
    if (user.wishlist.map(function(x) {return x.id}).includes(parseInt(id))) {
        button.html("REMOVE FROM WISHLIST");
    } else {
        button.html("ADD TO WISHLIST")
    }
    // On click add / remove item
    button.on("click", function(e) {
        var user = authenticationService.User();
        var _id = parseInt(id)
        e.preventDefault();
        if (user.wishlist.map(function(x) {return x.id}).includes(parseInt(id))) {
            authenticationService.removeWish(_id, function(success) {
                if (success) {
                    button.html("ADD TO WISHLIST");
                } else {
                    alert("Could not remove item");
                }
            });
        } else {
            authenticationService.addWish(_id, function(success) {
                if (success) {
                    button.html("REMOVE FROM WISHLIST");
                } else {
                    alert("Could not add item");
                }
            });
        }
    });
}

function setupFavoritesButton() {
    var button = $('#favorites_button');
    var user = authenticationService.User();
    
    // If no user, log in.
    if (!user) {
        button.on("click", function(e) {
            window.location.replace("/login");
        });
        return;
    }

    // Set up initial state
    if (user.favorites.map(function(x) {return x.id}).includes(parseInt(id))) {
        button.html("REMOVE FROM FAVORITES");
    } else {
        button.html("ADD TO FAVORITES")
    }
    // On click add / remove item
    button.on("click", function(e) {
        var user = authenticationService.User();
        var _id = parseInt(id)
        e.preventDefault();
        if (user.favorites.map(function(x) {return x.id}).includes(parseInt(id))) {
            authenticationService.removeFavorite(_id, function(success) {
                if (success) {
                    button.html("ADD TO FAVORITES");
                } else {
                    alert("Could not remove item");
                }
            });
        } else {
            authenticationService.addFavorite(_id, function(success) {
                if (success) {
                    button.html("REMOVE FROM FAVORITES");
                } else {
                    alert("Could not add item");
                }
            });
        }
    });
}

function setupcartListButton() {
    var button = $('#addtocart_button');
    var user = authenticationService.User();
    var cart = JSON.parse(localStorage.getItem("shoppingCart"));
    if(cart == null){
        cart = []
    }
    var _id = parseInt(id)
    var position = productInCart(_id, cart);

    //check if item is already in cart
    if (position > -1) {
        button.html("REMOVE FROM CART");
    } else {
        button.html("ADD TO CART")
    }
    // On click add / remove item
    button.on("click", function(e) {
        e.preventDefault();
        position = productInCart(_id, cart);
        if(position == -1){
            cart.push({id:_id, amount:1})
            button.html("REMOVE FROM CART");
        }else{
            cart.splice(position, 1)
            button.html("ADD TO CART");            
        }
        localStorage.setItem("shoppingCart", JSON.stringify(cart));
    });
}

function productInCart(id, cart){
    for(i=0; i<cart.length; i++){
        if(cart[i]['id'] == id){
            return i;
        }
    }
    return -1;
}