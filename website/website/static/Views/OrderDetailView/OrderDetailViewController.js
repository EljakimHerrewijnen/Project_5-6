var viewContainer = $("#view-container");
var pathname = $(location).attr('pathname');
var id = pathname.substring(pathname.lastIndexOf('/') + 1);
var order = {};

function onAssetsLoaded() {
    
}

// Adds the ProductListView.html to the DOM
function buildView(onComplete) {
    return function(){
        ajaxCall("/static/Views/OrderDetailView/OrderDetailView.html", "text", {}, function(_view) {
            var view = Handlebars.compile(_view);
            order["total_price"] = calculateTotal(order);
            viewContainer.append(view(order));
            onComplete();
        });
    }
}

// Retrieves the Products json and casts them to models.
function buildOrder(id, onComplete) {
    return function() {
        ajaxCall("/api/user/orders/" + id, "application/json", {}, function(json){
            json["product_id"] = id;
            order = json;
            onComplete();
        });
    }
}

$(document).ready(function(){   
    var pipeline = buildOrder(id, buildView(onAssetsLoaded));
    pipeline();
});


function calculateTotal (order) {
    return order.products.reduce(function (a, b) {
        return a + b.price;
    }, 0);
}