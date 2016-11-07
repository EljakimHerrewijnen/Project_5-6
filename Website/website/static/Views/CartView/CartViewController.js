var viewContainer = $("#view-container");
var cartcontents = []
function buildView() {
    ajaxCall("/static/Views/CartView/CartView.html", "text", {}, function(_view) {
        var view = $(_view);
        viewContainer.append(view);
        onViewLoad();
    });
}

function removedata(){

}

function storedata(name)
{    
    cartcontents = cartcontents + name;
    localStorage.setItem("cartcontents", cartcontents);
    window.alert(cartcontents);
    console.log("Done")
}

function getshoppingcart()
{
    var product = localStorage.getItem("product");
    console.log(product);
    var productobject = JSON.parse(product);
    return productobject
}

$(document).ready(function() {
    buildView()
});
