var NavBar = (() => {
    function NavBar() {
        var user = stateManager.getUser();
        user.then(() => {
            var logoutButton = $('#logout-button');
            logoutButton.html('<li class="nav-item nav-right">LOGOUT</li>');
        });

        this.toggleLogoutButton = function(turnOn) {
            var logoutButton = $('#logout-button');
            if (turnOn) {
                logoutButton.css({opacity: 0, width: 0});
                logoutButton.html('<li class="nav-item nav-right">LOGOUT</li>');
                logoutButton.animate({width: logoutButton.get(0).scrollWidth + 30}, 150).animate({opacity: 100}, 150);
            } else {
                logoutButton.empty();
                logoutButton.animate({opacity: 0}, 150).animate({width: 0}, 150);
            }
        }
    }
    return new NavBar()
})();