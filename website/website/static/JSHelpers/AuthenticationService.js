function AuthenticationService()
{
    var self = this;

    this.logout = function(){
        $.ajax({
            url: "/api/logout",
            method: "POST",
            success: function() {
                localStorage.clear();
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

    this.getUser = function(onDone) {
        $.ajax({
            url: "/api/user/account",
            method: "GET",
            error: function() {window.location.replace("/login")}
        }).done(function(x) {
            localStorage.setItem("user", JSON.stringify(x));
            console.log(x);
            onDone(x);
        });
    }

    this.refreshUser = function() {
        $.ajax({
        url: "/api/user/account",
        method: "GET"
        }).done(function(x) {
            console.log(x); 
            localStorage.setItem("user", JSON.stringify(x));
        });
    }
}

authenticationService = new AuthenticationService();