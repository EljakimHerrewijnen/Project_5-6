var auth = (() => {
    function auth() {
        var self = this;
        var user;

        this.login = function(username, password) {
            stateManager.clearUser();
            var data = JSON.stringify({"username": username, "password": password});
            var promise = $.post({
                url: "/api/login",
                method: "POST",
                data: data,
                contentType : "application/json",
                processData: false
            }).then(() => {
                NavBar.toggleLogoutButton(true);
                stateManager.getUser().then((user) => {
                    console.log(user)   
                    if (user.accountType === "admin") {
                        NavBar.toggleAdminButton(true);
                    }
                })
            });
            return promise;
        }

        this.createUser = function(user) {
            var user = JSON.stringify(user);
            promise = $.ajax({
                url: "/api/account",
                method: "POST",
                data: user,
                contentType : "application/json"
            });
            return promise;
        }

        this.logout = function(){
            $.ajax({
                url: "/api/logout",
                method: "POST"
            }).then((success) => {
                stateManager.clearUser();
                console.log(stateManager.hasUser());
                NavBar.toggleLogoutButton(false);
                NavBar.toggleAdminButton(false);
                viewManager.changeView(loginRegisterView);
            }, (failure) => {
                alert("Encountered an error when logging out");
                console.log(failure.response);
            });
        }
    }
    return new auth()
})();