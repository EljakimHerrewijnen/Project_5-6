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
    
    var getHtml = () => $.ajax({url: "/static/views/place-order-view.html",contentType: "text"});

    this.placeOrder = function() {
        var errorBox = $("#place-order-error-box");
        var postalCode = $("#dropDownAddres option:selected").attr('postal-code');
        var streetNumber = $("#dropDownAddres option:selected").attr('street-number');
        if (postalCode == undefined || streetNumber == undefined) {
            errorBox.removeClass('hidden');
            errorBox.html("No address selected. You can add a new address in your account settings page.");
            return;
        }
        var order = {
            address: {
                postalCode : postalCode,
                houseNumber: streetNumber,
            },
            items : Cart.items.map((x) => {return {quantity: x.quantity, id : x.product.id}})
        }

        $.post({url: "/api/account/order",
            contentType: "application/json",
            data: JSON.stringify(order)
        }).done( function(x) {
            alert("Placed order!");
            Cart.empty();
            stateManager.getUser().then((user) => {
                user.orders.push(x);
            });
            viewManager.redirect('/order/' + x.id)
        }).error((jqXHR) => {
            console.log(jqXHR);
        });
    }
}