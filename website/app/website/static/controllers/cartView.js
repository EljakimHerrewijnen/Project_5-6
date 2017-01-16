viewManager.addRoute("/cart", () => new cartView());

function cartView() {
    var self = this;

    Object.defineProperty(this, "url", {
        get : () => '/cart'
    });

    this.construct = function(newContainer) {
        container = newContainer;
        cart = stateManager.cart;
        var html = getHtml();
        var products = stateManager.getProducts();
        var cart = stateManager.getCartItems();

        promise = Promise.all([html, products]).then(([html, products]) =>{
            html = Handlebars.compile(html);
            container.append(html(products));
            container.css({opacity: 0});
        });

        return promise;
    }

    this.destruct = function() {
        return container.animate({opacity:0}, 150).promise().then(() => container.remove());
    }
    this.transitionIn =function() {
        container.animate({opacity: 1}, 150);
    }
    
    var getHtml = () => $.ajax({url: "http://localhost:5555/static/Views/CartView/CartView.html",contentType: "text"});
}

// Retrieves the Products json and casts them to models.
function getProduct(id, onComplete, entry) {
    ajaxCall("/API/Products/" + id, "application/json", {}, function(json){        
        product = json;
        onComplete(json, entry);
    });
}

function updateTotal() {
    $("#totalprice").html("€" + cartcontents.products.reduce(function(acc, val) {
        return acc + (val.price * val.amount);
    }, 0).toFixed(2));
}

function updateLocalStorageCart() {
    var cart = cartcontents.products.map(function(x) {
        return {"id" : x.product_id, "amount": x.amount}
    });
    localStorage.setItem("shoppingCart", JSON.stringify(cart));
}

function increment(id) {
    var i = cartcontents.products.find(function(x){
        return x.product_id == id;
    })
    i.amount = i.amount + 1;
    updateTotal();
    $("#cart-row-amount-" + id).html(i.amount);
    $("#cart-row-price-" + id).html("€" + (i.amount * i.price).toFixed(2));
    updateLocalStorageCart();
}

function decrement(id) {
    var i = cartcontents.products.find(function(x){
        return x.product_id == id;
    })
    if (i.amount == 1) return;
    i.amount = i.amount - 1;
    updateTotal();
    $("#cart-row-amount-" + id).html(i.amount);
    $("#cart-row-price-" + id).html("€" + (i.amount * i.price).toFixed(2));
    updateLocalStorageCart();
}

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

//}