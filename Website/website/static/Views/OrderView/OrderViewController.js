var viewContainer = $("#view-container");
var cartcontents = {"products" : []};
var product;
var totalPrice = 0;

function buildView() {
    ajaxCall("/static/Views/OrderView/OrderView.html", "text", {}, function(_view) {
        var view = Handlebars.compile(_view);
        console.log(cartcontents);
        viewContainer.append(view(cartcontents));
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
    authenticationService.getUser(test);
    totalPrice = cartcontents.products.reduce(function(acc, x) {return acc + parseFloat(x.price)}, 0);
    console.log(totalPrice);
    totalprice();
}

$(document).ready(function() {
    var cart = JSON.parse(localStorage.getItem("shoppingCart"));
    cart = cart.map(function(x) {return x['id']});
    ajaxCall("/API/Products", "application/json", {}, function(json){
        var shop = JSON.parse(localStorage.getItem("shoppingCart"));
        json = json.map(function(x) { x["price"] = x["price"].toFixed(2); return x;})
        cartcontents["products"] = json.filter(function(x) {
            return cart.includes(x.product_id);
        });      
        cartcontents.products.forEach(function(x) {
            var i = cart.indexOf(x.product_id);
            if (i != -1) {
                x["amount"] = shop[i]["amount"]
            }
        });
        buildView();
    });  
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
        
        var name = document.createTextNode(product.name)
        // var amount = document.createTextNode("")    
        var amount = document.createElement("div");
        amount.className = "Amount";
        amount.innerHTML = entry['amount'];
        var price = document.createTextNode("€ " + (entry.amount * product.price).toFixed(2))
        totalPrice = totalPrice + product.price * entry.amount;
        totalprice();

        nameCell.appendChild(name)
        amountCell.appendChild(amount)
        priceCell.appendChild(price)
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
}

function goToOrder()
{
    var user = authenticationService.User();
    
    // If no user, log in.
    if (!user) {
        //redirect to login
        window.location.replace("/login"); 
    }else{
        //go to confirm order page
    
        window.location.replace("/orderview"); 
    }
        
}

function displayAddress() {
    authenticationService.getUser(test);
}

function test(user){
    var addresses = user.addresses;
    var dropdown ="";
    for(var i =0; i < addresses.length; i++){
        dropdown += "<option value="+addresses[i].postal_code + "_" + addresses[i].house_number + ">" + addresses[i].city + ", " + addresses[i].street + " " + addresses[i].house_number + "</option>"
    }
    document.getElementById("dropDownAddres").innerHTML = dropdown;   
}

function sendToDatabase(user){
    var dropdownvalue = $("#dropDownAddres").val();
    var postal_code = dropdownvalue.split("_");
    var cart = JSON.parse(localStorage.getItem("shoppingCart"));
    var order = {
        address:{
            postal_code: postal_code[0],
            house_number: postal_code[1]
        },
       items:cart
    }
    order = JSON.stringify(order);
    $.ajax({url: "/api/user/orders",
            method: "POST",
            contentType: "application/json",
            data: order
            }).done( function(x) {
                localStorage.clear("shoppingCart");
                window.location.replace("/account");
    });
}
//}