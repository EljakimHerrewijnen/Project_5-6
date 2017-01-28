
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
            snackbar.addClass('open');
        }

        this.toggle = function() {
            menuBar.toggleClass('open');
            backDrop.toggleClass('open');
        }

        this.update = function(amount) {
            if (amount < 1) {
                this.hide();
            } else if (amount == 1) {
                this.show();
                text.addClass('glow');
                text.removeClass('glow');
                text.html(amount + " item in your cart")
            } else {
                this.show();
                text.addClass('glow');
                text.removeClass('glow');
                text.html("<b>" + amount + "</b> items in your cart")
            }
        }

        this.setMessage = function(message) {

        }

        this.setAction = function(action) {
            actionButton.unbind();
            actionButton.click(action);
        }
    }
    return new Snackbar()
})();