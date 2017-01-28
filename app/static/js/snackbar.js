var Snackbar = (() => {
    function Snackbar() {
        var self = this;
        var snackbar = $('#snackbar');
        var text = $('#snackbar-text');
        var actionButton = $('#snackbar-action');

        this.hide = function() {
            snackbar.removeClass('open')
        }

        this.show = function() {
            var activeView = ViewManager.activeView;
            if (activeView) {
                var url = activeView.url
                if (url == '/placeorder' || url == '/cart')
                    return;
            }
            snackbar.addClass('open');
        }

        this.toggle = function() {
            menuBar.toggleClass('open');
            backDrop.toggleClass('open');
        }

        this.tickle = function() {
        }

        this.update = function(amount) {
            amount = Cart.quantity;
            if (amount < 1 || amount == undefined) {
                this.hide();
            } else if (amount == 1) {
                this.show();
                text.addClass('glow');
                text.removeClass('glow');
                text.html("<b>" + amount + "</b>&#160;Item in your cart")
            } else {
                this.show();
                text.addClass('glow');
                text.removeClass('glow');
                text.html("<b>" + amount + "</b>&#160;Items in your cart")
            }
        }

        this.setAction = function(action) {
            actionButton.unbind();
            actionButton.click(action);
        }
    }
    return new Snackbar()
})();