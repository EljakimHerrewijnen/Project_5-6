// Global variables.
var product;
var viewContainer = $("#view-container");
var pathname = $(location).attr('pathname');
var id = pathname.substring(pathname.lastIndexOf('/') + 1);
var cartcontents;

function onAssetsLoaded() {
    setupWishListButton();
    setupFavoritesButton();
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
            product = json;
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
    var productname = document.getElementById("cartbutton").value;
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
                    button.html("FAVORITE");
                } else {
                    alert("Could not remove item");
                }
            });
        } else {
            authenticationService.addFavorite(_id, function(success) {
                if (success) {
                    button.html("UNFAVORITE");
                } else {
                    alert("Could not add item");
                }
            });
        }
    });
}

