function AuthenticationService()
{
    var self = this;
    var key;

    var getJsonToken = function(email, password) {
        function printTest(data, textStatus, jqXHR)
        {
            console.log(data);
        }

        function tokenHandler(data, textStatus, jqXHR) {
            console.log(data);
            key = data;
            $.get("/API/AuthTest", {}, printTest, "text")
        }

        $.post('/API/Authenticate', {'email': email, 'password': password}, tokenHandler, "text");
    }

    this.logout = function(){

    }

    this.attemptLogin = function(email, password ,onSuccess, onFailure) {
        getJsonToken(email, password);
    }

    this.signData = function(data) {
        return data;
    }

    this.createUser = function(user, onSuccess, onFailure)
    {
        $.ajax({
            url: "/API/User",
            method: "POST",
            data: user,
            success: onSuccess,
            error: onFailure
        })
    }
}

authenticationService = new AuthenticationService();