function AuthenticationService()
{
    var self = this;
    var key;


    function tokenHandler(data, textStatus, jqXHR) {
        key = data;
    }

    this.logout = function(){

    }

    this.attemptLogin = function(username, password, onDone, onFailure) {
        var formdata = new FormData();
        formdata.append("password", password);
        formdata.append("username", username);
        
        $.ajax({
            url: "/api/login",
            method: "POST",
            data: formdata,
            processData: false,
            success: onDone,
            error: onFailure
        });
    }

    this.signData = function(data) {
        return data;
    }

    this.createUser = function(user, onSuccess, onFailure)
    {
        $.ajax({
            url: "/api/account",
            method: "POST",
            data: user,
            success: onSuccess,
            error: onFailure
        })
    }
}

authenticationService = new AuthenticationService();