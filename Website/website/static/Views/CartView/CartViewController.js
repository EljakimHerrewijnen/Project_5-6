var viewContainer = $("#view-container");
var cartcontents = []
var product

function buildView() {
    ajaxCall("/static/Views/CartView/CartView.html", "text", {}, function(_view) {
        var view = $(_view);
        viewContainer.append(view);
        onViewLoad();
    });
}

// Retrieves the Products json and casts them to models.
function getProduct(id, onComplete) {
    console.log(1)
    // return function() {
        ajaxCall("/API/Products/" + id, "application/json", {}, function(json){
        console.log(2)
            
            product = json;
            onComplete(json);
        });
    // }
}

function onViewLoad(){
    buildTable();
}


$(document).ready(function() {
    buildView();
});

function buildTable(){
    var table = document.getElementById('orderTable').getElementsByTagName('tbody')[0];
    var cart = JSON.parse(localStorage.getItem("shoppingCart"));    
console.log(cart);
    cart.forEach(function(entry){
        test = getProduct(entry, addrow);
        // test();
    });
function addrow(product){
console.log(product);
    var newRow = table.insertRow(table.rows.length);
    var nameCell = newRow.insertCell(0);
    var amountCell = newRow.insertCell(1);
    var priceCell = newRow.insertCell(2);
    var removeCell = newRow.insertCell(3);
    
    var name = document.createTextNode(product.name)
    var amount = document.createTextNode("")    
    var price = document.createTextNode("€" + product.price)
    var remove = document.createElement("div");
    remove.className = "Amount";
    remove.innerHTML = "<a onclick='removeCartItem(product.id)'>Remove lol</a>";

    nameCell.appendChild(name)
    amountCell.appendChild(amount)
    priceCell.appendChild(price)
    removeCell.appendChild(remove)
}    
}

function removeCartItem(id){
    var cart = JSON.parse(localStorage.getItem("shoppingCart"));

    position = cart.indexOf(id)
    cart.splice(position)
    localStorage.setItem("shoppingCart", JSON.stringify(cart));
    location.reload();
}
