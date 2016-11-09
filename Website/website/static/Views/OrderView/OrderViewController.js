var viewContainer = $("#view-container");
var cartcontents = [];
var product;
var totalPrice = 0;


function buildView() {
    ajaxCall("/static/Views/OrderView/OrderView.html", "text", {}, function(_view) {
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
    displayAddress();
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
        console.log(3); 
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
        console.log(addresses[i]);
        dropdown += "<option value="+addresses[i].postal_code + "_" + addresses[i].house_number + ">" + addresses[i].city + ", " + addresses[i].street + " " + addresses[i].house_number + "</option>"
    }
    document.getElementById("dropDownAddres").innerHTML = dropdown;   
}

function sendToDatabase(user)
{
    var dropdownvalue = $("#dropDownAddres").val();
    console.log(dropdownvalue);
    var items = localStorage
    var postal_code = dropdownvalue.split("_");
    var order = {
        "address":{
            "postal_code": postal_code[0],
            "house_number": postal_code[1]
        }
      //  "items"
        // address: {postal_code[0] + postal_code[1]}

    }

    values = dropdownvalue;
    // $.ajax({url: "/api/user/orders",
    //         method: "POST",
    //         contentType: "aplication/json",
    //         data: values
    //         })

}
//}