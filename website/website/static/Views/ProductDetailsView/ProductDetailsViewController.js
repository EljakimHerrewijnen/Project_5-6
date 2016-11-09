// Global variables.
var product;
var viewContainer = $("#view-container");
var pathname = $(location).attr('pathname');
var id = pathname.substring(pathname.lastIndexOf('/') + 1);
var cartcontents;

function onAssetsLoaded() {
    setupWishListButton();
    setupFavoritesButton();
    setupcartListButton();
}

// Adds the ProductListView.html to the DOM
function buildView(onComplete) {
    return function(){
        ajaxCall("/static/Views/ProductDetailsView/ProductDetailsView.html", "text", {}, function(_view) {
            var view = Handlebars.compile(_view);
            viewContainer.append(view(product));
            onComplete();
        });
    }
}

// Retrieves the Products json and casts them to models.
function buildProduct(id, onComplete) {
    return function() {
        ajaxCall("/API/Products/" + id, "application/json", {}, function(json){
            json["product_id"] = id;
            product = jsonToProduct(json);
            onComplete();
        });
    }
}

$(document).ready(function(){   
    var pipeline = buildProduct(id, buildView(onAssetsLoaded));
    pipeline();
}); 

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

function setupWishListButton() {
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
    if (user.wishList.map(function(x) {return x.product_id}).includes(parseInt(id))) {
        button.html("REMOVE FROM WISHLIST");
    } else {
        button.html("ADD TO WISHLIST")
    }
    // On click add / remove item
    button.on("click", function(e) {
        var user = authenticationService.User();
        var _id = parseInt(id)
        e.preventDefault();
        if (user.wishList.map(function(x) {return x.product_id}).includes(parseInt(id))) {
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
    if (user.favorites.map(function(x) {return x.product_id}).includes(parseInt(id))) {
        button.html("REMOVE FROM FAVORITES");
    } else {
        button.html("ADD TO FAVORITES")
    }
    // On click add / remove item
    button.on("click", function(e) {
        var user = authenticationService.User();
        var _id = parseInt(id)
        e.preventDefault();
        if (user.favorites.map(function(x) {return x.product_id}).includes(parseInt(id))) {
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