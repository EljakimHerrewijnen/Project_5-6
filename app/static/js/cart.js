var Cart = (() => {
    function Cart() {
        var self = this;
        var items = []
        this.empty = () => {
            items = []
            localStorage.setItem("cartItems", "[]");
        };

        Object.defineProperty(this, "isEmpty", {
            get : () => items.length == 0
        });

        Object.defineProperty(this, "items", {
            get : () => items
        });

        Object.defineProperty(this, "quantity", {
            get : () => items.reduce((acc, item) => acc + item.quantity, 0)
        });

        this.getTotalPrice = function() {
            var total = items.map((item) => 
                item.product.price * item.quantity
            ).reduce(
                (acc, v) => acc + v
            ,0);
            return total;
        }

        this.getItem = function(id) {
            var item = items.find((item) => 
                item.product.id == id
            );
            return item;
        }

        this.addById = function(id) {
            stateManager.getProducts().then((products) => {
                var product = products.find((x) => x.id == id);
                if (product)
                    self.addProduct(product);
            });
        }

        this.addProduct = function(product) {
            var item = this.getItem(product.id);
            if (item != undefined) {
                item.quantity++;
            } else {
                item = {
                    quantity: 1,
                    product : product
                }
                items.push(item);
            }
            this.saveInLocalStorage();
            Snackbar.update();
        }

        this.increment = function(id, quantity) {
            var item = this.getItem(id);
            item.quantity = item.quantity + quantity;
            if (item.quantity < 1)
                this.removeProduct(item.product.id);
            this.saveInLocalStorage();
            Snackbar.update();
        }

        this.removeProduct = function(id) {
            items = items.filter((item) => 
                item.product.id != id
            )
            this.saveInLocalStorage();
            Snackbar.update();
        }
        
        this.getquantity = function(id) {
            var item = this.getItem(id);
            return item.quantity;
        }

        this.getItemPrice = function(id) {
            var item = this.getItem(id);
            return item.quantity * item.product.price;
        }

        this.saveInLocalStorage = function() {
            var stringifiedItems = JSON.stringify(items);
            localStorage.setItem('cartItems', stringifiedItems);
        };

        this.getFromLocalStorage = function() {
            items = [];
            try {
                storage = JSON.parse(localStorage.getItem('cartItems'))
                for (var i in storage) {
                    var item = storage[i]
                    item.product = new Product(item.product);
                    items.push(item);
                }
            } catch(err) {
                console.log("Could not get cart items from local storage, setting to empty cart!");
                items = [];
            }  
            return items;
        };
        items = this.getFromLocalStorage();
    }
    return new Cart()
})();