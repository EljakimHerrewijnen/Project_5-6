var stateManager = (() => {
    function singleton() {
        var products;
        var cart = {"products" : []};
        var user;

        this.getUser = function() {
            if (this.hasUser()) return Promise.resolve(user);
            req = $.ajax({url: "/api/account", method: "GET"});
            req = req.then((response) => {
                user = new User(response);
                localStorage.setItem('user', user.string);
                return user;
            });
            return req;
        }

        this.hasUser = () => user != undefined;
        
        this.clearUser = () => {
            user = undefined;
            localStorage.removeItem('user');
        }

        this.getProducts = () => {
            if (products) return Promise.resolve(products);
            rawProducts = $.ajax({url: "/api/products", contentType: "application/json"});
            return rawProducts.then((data) => {
                products = data.map(jsonToProduct);
                return products;
            });
        }

        this.getCartItems = () => {
            return cart;
        }

        this.verifyForm = function verifyForm(form, errorBox) {
            var inputs = form.find('input');
            r = true
            errorBox.html("");
            errorBox.addClass('hidden');
            for (var i = 0; i < inputs.length; i++) {
                console.log(inputs[i]);
                var input = $(inputs[i]);
                var required = input.is(':required');
                var verificationRegex = input.attr('verification');
                var value = input.val()
                input.removeClass("error");
                if (required && (value == undefined || value == ""))
                {
                    r = false
                    input.addClass("error");
                }   
                if (verificationRegex)
                {
                    re = new RegExp("^" + verificationRegex + "$");
                    if (!re.test(value)) {
                        
                        input.addClass("error");
                        r = false
                    }
                }
            }
            if (errorBox && !r) {
                errorBox.html("Please check if all fields are and filled in and have a correct value.");
                errorBox.removeClass('hidden');
            }
            return r;
        }

    }
    return new singleton();
})();