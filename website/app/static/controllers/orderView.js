var viewContainer = $("#view-container");
var pathname = $(location).attr('pathname');
var id = pathname.substring(pathname.lastIndexOf('/') + 1);
var order = {};

viewManager.addRoute('/order/\\d+', (path) => {
    var orderId = path.split('/').pop();
    return new orderView(orderId);
});

function orderView(orderId) {
    var self = this;
    var container;

    Object.defineProperty(this, "url", {
        get : () => '/order/' + orderId
    });

    this.construct = function(newContainer) {
        container = newContainer;
        var html = getHtml();
        var order = getOrder(orderId);

        return Promise.all([html, order]).then(([html, order]) => {
            container.css({opacity: 0})
            html = Handlebars.compile(html);
            order['total_price'] = order.products.reduce((total, product) => total + product.price * product.quantity, 0);
            container.append(html(order));
        });
    }

    this.destruct = function() {
        return container.animate({opacity: 0}, 150).promise().then(() => container.remove());
    }

    this.transitionIn = function() {
        container.animate({opacity: 1}, 150);
    }

    var getHtml = () => $.ajax({url: "/static/views/order-view.html",contentType: "text"});
    var getOrder = (orderId) => $.ajax({url: "/api/user/orders/" + orderId ,contentType: "application/json"});
}