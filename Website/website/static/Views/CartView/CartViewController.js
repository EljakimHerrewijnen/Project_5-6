function buildView() {
    ajaxCall("/static/Views/CartView/CartView.html", "text", {}, function(_view) {
        var view = $(_view);
        viewContainer.append(view);
        onViewLoad();
    });
}

function storedata(id, name, description)
{
    window.alert("hello")
    localStorage.setItem("product", id, name, description);
}

function getshoppingcart()
{
    var product = localStorage.getItem("product");
    console.log(product);
    var productobject = JSON.parse(product);
}
