// Global variables.
var product;
var viewContainer = $("#view-container");
var pathname = $(location).attr('pathname');
var id = pathname.substring(pathname.lastIndexOf('/') + 1);

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
    //window.alert("hello");    
    localStorage.setItem("name", productname);
    var namestorage = localStorage.getItem("name");
    window.alert(namestorage);
}
