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
                products = data.map((x) => new Product(x));
                return products;
            });
        }

        this.getCartItems = () => {
            return cart;
        }

        this.submitVerify = function(form) {
            form = $(form);
            var inputs = form.find('input');
            var errorBox = form.find('.error-box');
            var validated = true;
            inputs.each((x) => {
                var input = $(inputs[x]);

                var verificationRegex = input.attr('verification');
                if (validated)
                    validated = verifyInputField(input);
                else
                    verifyInputField(input);
            });
            if (errorBox) {
                errorBox.removeClass('hidden');
                if (!validated)
                    errorBox.html("Please check if all fields are and filled in and have a correct value.");
                else
                    errorBox.removeClass('hidden');
            }
            return validated;
        }

        var verifyInputField = function(input) {
            var input = $(input);
            var value = input.val();
            var verificationRegex = input.attr('verification');
            var re = new RegExp("^" + verificationRegex + "$");
            var isRequired = input.is(':required');
            if ((verificationRegex && !re.test(value)) || (isRequired && !value)) {
                input.closest('.md-input-field').addClass('error');
                return false;
            } else {
                input.closest('.md-input-field').removeClass('error');
                return true;
            }
        }

        var jqueryFix = function() {
            verifyInputField(this);
        }

        this.addRealtimeVerify = function(form) {
            var form = $(this);
            var inputs = form.find('input');
            inputs.each((x) => {
                var input = $(inputs[x]);
                var isRequired = input.is(':required');
                var verificationRegex = input.attr('verification');
                if (isRequired && verificationRegex)
                    input.on('change', jqueryFix);
            });
        }
    }
    return new singleton();
})();

