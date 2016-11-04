var viewContainer = $("#view-container");

function buildView() {
    ajaxCall("/static/Views/CartView/CartView.html", "text", {}, function(_view) {
        var view = $(_view);
        viewContainer.append(view);
        onViewLoad();
    });
}

function storedata(product)
{
    localStorage.setItem("product", product);
}

function getshoppingcart()
{
    var product = localStorage.getItem("product");
    console.log(product);
    var productobject = JSON.parse(product);
}

$(document).ready(function() {
    buildView()
});