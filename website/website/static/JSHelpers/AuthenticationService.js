function AuthenticationService()
{
    var self = this;
    var user = null;

    this.logout = function(){
        $.ajax({
            url: "/api/logout",
            method: "POST",
            success: function() {
                localStorage.clear();
                user = null;
                window.location.replace("/login")
            }
        });
    }

    this.attemptLogin = function(username, password, onDone, onFailure) {
        values = {
            "username" : username,
            "password" : password
        }
        values = JSON.stringify(values);
        
        $.ajax({
            url: "/api/login",
            method: "POST",
            data: values,
            contentType : "application/json",
            processData: false,
            success: onDone,
            error: onFailure
        }).Done(function(x) {
            getUser(function(u){
                self.user = u;
            });
        });
    }

    this.updateUser = function(user, onSuccess, onFailure) {
        $.ajax({
            url: "/api/user/account",
            method: "PUT",
            contentType : "application/json",
            data: user,
            success: onSuccess,
            error: onFailure
        })
    }

    this.createUser = function(user, onSuccess, onFailure)
    {
        $.ajax({
            url: "/api/user/account",
            method: "POST",
            contentType : "application/json",
            data: user,
            success: onSuccess,
            error: onFailure
        })
    }

    this.User = function() {
        if (user) return user;
        user = JSON.parse(localStorage.getItem("user"))
        if (user) return user;
        return null;
    }

    this.getUser = function(onDone) {
        $.ajax({
            url: "/api/user/account",
            method: "GET",
            error: function() {window.location.replace("/login")}
        }).done(function(x) {
            localStorage.setItem("user", JSON.stringify(x));
            user = x;
            onDone(x);
        });
    }

    this.refreshUser = function() {
        $.ajax({
        url: "/api/user/account",
        method: "GET"
        }).done(function(x) {
            user = x;
            localStorage.setItem("user", JSON.stringify(x));
        });
    }

    this.addWish = function(product_id, callback) {
        if (!self.User()) window.location.replace("/login");
        value = JSON.stringify({"product_id" : product_id});
        $.ajax({
            url: "/api/user/wishlist",
            method: 'POST',
            contentType : "application/json",
            data: value,
            success: function(e) {
                self.refreshUser();
                callback(true);
            },
            error: function(e) {callback(false)}
        });
    }

    this.removeWish = function(product_id, callback) {
        if (!self.User()) window.location.replace("/login");
        value = JSON.stringify({"product_id" : product_id});
        $.ajax({
            url: "/api/user/wishlist",
            method: 'DELETE',
            contentType : "application/json",
            data: value,
            success: function(e) {
                self.refreshUser();
                callback(true);
            },
            error: function(e) {callback(false)}
        });
    }

    this.addFavorite = function(product_id, callback) {
        if (!self.User()) window.location.replace("/login");
        value = JSON.stringify({"product_id" : product_id});
        $.ajax({
            url: "/api/user/favorites",
            method: 'POST',
            contentType : "application/json",
            data: value,
            success: function(e) {
                self.refreshUser();
                callback(true);
            },
            error: function(e) {callback(false)}
        });
    }

    this.removeFavorite = function(product_id, callback) {
        if (!self.User()) window.location.replace("/login");
        value = JSON.stringify({"product_id" : product_id});
        $.ajax({
            url: "/api/user/favorites",
            method: 'DELETE',
            contentType : "application/json",
            data: value,
            success: function(e) {
                self.refreshUser();
                callback(true);
            },
            error: function(e) {callback(false)}
        });
    }

    this.togglePublicWishlist = function(toggle, callback) {
        if (!self.User()) window.location.replace("/login");
        value = JSON.stringify({"wishlist_public" : toggle});
        $.ajax({
            url: "/api/user/account",
            method: 'PUT',
            contentType : "application/json",
            data: value,
            success: function(e) {
                self.refreshUser();
                callback(true);
            },
            error: function(e) {callback(false)}
        });
    }
}

authenticationService = new AuthenticationService();