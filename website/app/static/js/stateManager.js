var stateManager = (() => {
    function singleton() {
        var products;
        var cart = {"products" : []};
        var user;

        this.getUser = function() {
            if (this.hasUser()) return Promise.resolve(user);
            req = $.ajax({url: "/api/user/account", method: "GET"});
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
            rawProducts = $.ajax({url: "http://localhost:5555" + "/api/products", contentType: "application/json"});
            return rawProducts.then((data) => {
                products = data.map(jsonToProduct);
                return products;
            });
        }

        this.getCartItems = () => {
            return cart;
        }
    }
    return new singleton();
})();