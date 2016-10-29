// Global variables.
var product;
var viewContainer = $("#view-container");

function onAssetsLoaded() {

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
        ajaxCall("/API/Products/1", "application/json", {}, function(json){
            product = json;
            onComplete();
        });
    }
}

$(document).ready(function(){   
    var pipeline = buildProduct(1, buildView(onAssetsLoaded));
    pipeline();
});