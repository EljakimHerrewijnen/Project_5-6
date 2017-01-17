viewManager.addRoute("/placeorder", () => new placeOrderView());

function placeOrderView() {
    var self = this;

    Object.defineProperty(this, "url", {
        get : () => '/placeorder'
    });

    this.construct = function(newContainer) {
        container = newContainer;
        var html = getHtml();
        var user = stateManager.getUser();
        var items = Cart.items

        promise = Promise.all([html, user]).then(([html, user]) => {
            html = Handlebars.compile(html);
            console.log(items);
            container.append(html({items: items, addresses: user.addresses, totalPrice: Cart.getTotalPrice()}));
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
    
    var getHtml = () => $.ajax({url: "http://localhost:5555/static/views/place-order-view.html",contentType: "text"});
}

function placeOrder() {
    var postalCode = $("#dropDownAddres option:selected").attr('postal-code');
    var streetNumber = $("#dropDownAddres option:selected").attr('street-number');
    var order = {
        address: {
            postal_code : postalCode,
            house_number: streetNumber,
        },
        items : Cart.items.map((x) => {return {amount: x.amount, id : x.product.id}})
    }

    $.post({url: "/api/user/orders",
        contentType: "application/json",
        data: JSON.stringify(order)
    }).done( function(x) {
            alert("Placed order!");
            Cart.empty();
            viewManager.redirect('/account')
    }).error((jqXHR) => {
        console.log(jqXHR);
    });
}