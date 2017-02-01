var NavBar = (() => {
    function NavBar() {
        var user = stateManager.getUser();
        user.then((user) => {
            var logoutButton = $('#logout-button');
            logoutButton.html('<li class="nav-item nav-right">LOGOUT</li>');
            if (user.accountType == "admin"){
                var adminButton = $('#admin-button');
                adminButton.html('<li class="nav-item nav-right">ADMIN</li>');
            }
        });

        this.toggleLogoutButton = function(turnOn) {
            MobileNavBar.toggleLogoutButton(turnOn);
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

        this.toggleAdminButton = function(turnOn) {
            MobileNavBar.toggleAdminButton(turnOn);
            var adminButton = $('#admin-button');
            if (turnOn) {
                adminButton.css({opacity: 0, width: 0});
                adminButton.html('<li class="nav-item nav-right">ADMIN</li>');
                adminButton.animate({width: adminButton.get(0).scrollWidth + 30}, 150).animate({opacity: 100}, 150);
            } else {
                adminButton.empty();
                adminButton.animate({opacity: 0}, 150).animate({width: 0}, 150);
            }
        }
    }
    return new NavBar()
})();


$('#mobile-search-button').click((e) => {
    viewManager.changeView(ProductListView);
    SideBar.toggle();
})


$('#mobile-menu-button').click((e) => {
    MobileMenuBar.toggle();
})