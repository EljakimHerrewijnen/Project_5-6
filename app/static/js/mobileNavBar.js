var MobileNavBar = (() => {
    function MobileNavBar() {
        var user = stateManager.getUser();
        user.then((user) => {
            var logoutButton = $('#mobile-logout-button');
            logoutButton.html('<span>Logout</span>');
            if (user.accountType == "admin"){
                var adminButton = $('#mobile-admin-button');
                adminButton.html('<span>Admin</span>');
            }
        });

        this.toggleLogoutButton = function(turnOn) {
            var logoutButton = $('#mobile-logout-button');
            if (turnOn) {
                logoutButton.html('<span>Logout</span>');
            } else {
                logoutButton.empty();
            }
        }

        this.toggleAdminButton = function(turnOn) {
            var adminButton = $('#mobile-admin-button');
            if (turnOn) {
                adminButton.html('<span>Admin</span>');
            } else {
                adminButton.empty();
            }
        }
    }
    return new MobileNavBar()
})();