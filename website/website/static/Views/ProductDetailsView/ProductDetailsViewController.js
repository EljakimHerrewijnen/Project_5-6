// Global variables.
var product;
var viewContainer = $("#view-container");
var pathname = $(location).attr('pathname');
var id = pathname.substring(pathname.lastIndexOf('/') + 1);

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

function setupWishListButton() {
    var user = JSON.parse(localStorage.getItem("user"));
    var button = $('#wishlist_button');
    if (!user) {
        button.on("click", function(e) {
            window.location.replace("/login");
        });
        return;
    }

    value = JSON.stringify({ "product_id" : parseInt(id) });
    if (user.wishList.map(function(x) {return x.product_id}).includes(parseInt(id))) {
        button.html("REMOVE FROM WISHLIST");
    } else {
        button.html("ADD TO WISHLIST")
    }


    button.on("click", function(e) {
        var user = JSON.parse(localStorage.getItem("user"));
        e.preventDefault();
        if (user.wishList.map(function(x) {return x.product_id}).includes(parseInt(id))) {
            $.ajax({
            url: "/api/user/wishlist",
            method: 'DELETE',
            contentType : "application/json",
                data: value,
                success: authenticationService.getUser(function(e) {
                    user = e;
                    console.log(e);
                    button.html("ADD TO WISHLIST");
                }),
                error: function(e) {alert(e)}
            });
        } else {
            $.ajax({
            url: "/api/user/wishlist",
            method: 'POST',
            contentType : "application/json",
                data: value,
                success: authenticationService.getUser(function(e) {
                    user = e;
                    console.log(e);
                    button.html("REMOVE FROM WISHLIST");
                }),
                error: function(e) {alert(e)}
            });
        }
    });
}


function setupFavoritesButton() {
    var user = JSON.parse(localStorage.getItem("user"));
    var button = $('#favorites_button');
    if (!user) {
        button.on("click", function(e) {
            window.location.replace("/login");
        });
        return;
    }

    value = JSON.stringify({ "product_id" : parseInt(id) });
    if (user.favorites.map(function(x) {return x.product_id}).includes(parseInt(id))) {
        button.html("UNFAVORITE");
    } else {
        button.html("FAVORITE")
    }


    button.on("click", function(e) {
        var user = JSON.parse(localStorage.getItem("user"));
        e.preventDefault();
        if (user.favorites.map(function(x) {return x.product_id}).includes(parseInt(id))) {
            console.log("IN LIST");
            $.ajax({
            url: "/api/user/favorites",
            method: 'DELETE',
            contentType : "application/json",
                data: value,
                success: authenticationService.getUser(function(e) {
                    user = e;
                    console.log(e);
                    button.html("FAVORITE");
                }),
                error: function(e) {alert(e)}
            });
        } else {
            console.log("NOT IN LIST");
            $.ajax({
            url: "/api/user/favorites",
            method: 'POST',
            contentType : "application/json",
                data: value,
                success: authenticationService.getUser(function(e) {
                    user = e;
                    console.log(e);
                    button.html("UNFAVORITE");
                }),
                error: function(e) {alert(e)}
            });
        }
    });
}