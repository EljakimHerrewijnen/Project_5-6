var viewContainer = $("#view-container");
var cartcontents = [];
var product;
var totalPrice = 0;

function buildView() {
    ajaxCall("/static/Views/CartView/CartView.html", "text", {}, function(_view) {
        var view = $(_view);
        viewContainer.append(view);
        onViewLoad();
    });
}

// Retrieves the Products json and casts them to models.
function getProduct(id, onComplete, entry) {
    ajaxCall("/API/Products/" + id, "application/json", {}, function(json){        
        product = json;
        onComplete(json, entry);
    });
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

    if(cart.length == 0){
        document.getElementById('orderDiv').style.display = "none";
        document.getElementById('emptyCart').style.display = "";
    }else{
        cart.forEach(function(entry){
            getProduct(entry['id'], addRow, entry);        
        });
    }
    //add row to table of products in cart
    function addRow(product, entry){
        var newRow = table.insertRow(table.rows.length);
        var nameCell = newRow.insertCell(0);
        var amountCell = newRow.insertCell(1);
        var priceCell = newRow.insertCell(2);
        var removeCell = newRow.insertCell(3);
        
        var name = document.createTextNode(product.name)
        // var amount = document.createTextNode("")    
        var amount = document.createElement("div");
        amount.className = "Amount";
        amount.innerHTML = "<input onchange='updateAmount("+product.id+", value)'  type='number' min='1' max='9' maxlength='1' placeholder='Amount'      value='"+entry['amount']+"' name='name'>";
        var price = document.createTextNode("€ " + (entry.amount * product.price).toFixed(2))
        totalPrice = totalPrice + product.price * entry.amount;
        totalprice();
        var remove = document.createElement("div");
        remove.className = "RemoveButton";
        remove.innerHTML = "<a onclick='removeCartItem("+product.id+")'>Remove</a>";

        nameCell.appendChild(name)
        amountCell.appendChild(amount)
        priceCell.appendChild(price)
        removeCell.appendChild(remove)
    }
}

function removeCartItem(id){
    var cart = JSON.parse(localStorage.getItem("shoppingCart"));

    position = productInCart(id, cart);
    cart.splice(position, 1);
    localStorage.setItem("shoppingCart", JSON.stringify(cart));
    location.reload();
}

function updateAmount(id, value){
    if(value < 10){
        var cart = JSON.parse(localStorage.getItem("shoppingCart"));
        index = productInCart(id, cart)
        cart[index]['amount'] = value
        localStorage.setItem("shoppingCart", JSON.stringify(cart));
        location.reload();
    }else{
        window.alert("You cannot buy more than 9 products")
    }
   
}

function productInCart(id, cart){
    for(i=0; i<cart.length; i++){
        if(cart[i]['id'] == id){
            return i;
        }
    }
    return -1;
}

//Total price
function totalprice()
{
    document.getElementById('totalprice').innerHTML =" € " + totalPrice.toFixed(2);
    // totalprice.innerHTML(totalPrice);
    // document.getElementById('totalprice').innerHTML("Total price= €" + totalPrice)
}
