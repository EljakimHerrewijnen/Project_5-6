var viewContainer = $("#view-container");
var pathname = $(location).attr('pathname');
var id = pathname.substring(pathname.lastIndexOf('/') + 1);
var product = {};

function onAssetsLoaded() {
    
}

// Adds the ProductListView.html to the DOM
function buildView(onComplete) {
    return function(){
        ajaxCall("/static/Views/OrderDetailView/OrderDetailView.html", "text", {}, function(_view) {
            var view = Handlebars.compile(_view);
            viewContainer.append(view(product));
            onComplete();
        });
    }
}

// Retrieves the Products json and casts them to models.
function buildProduct(id, onComplete) {
    return function() {
        ajaxCall("/api/user/orders/" + id, "application/json", {}, function(json){
            json["product_id"] = id;
            product = json;
            onComplete();
        });
    }
}

$(document).ready(function(){   
    var pipeline = buildProduct(id, buildView(onAssetsLoaded));
    pipeline();
});
