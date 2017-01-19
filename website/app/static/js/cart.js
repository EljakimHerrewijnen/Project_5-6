var Cart = (() => {
    function Cart() {
        var self = this;
        var items = []
        this.empty = () => {
            items = []
            localStorage.setItem("cartItems", "[]");
        };
        

        Object.defineProperty(this, "items", {
            get : () => items
        });

        this.getTotalPrice = function() {
            var total = items.map((item) => 
                item.product.price * item.amount
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

        this.addProduct = function(product) {
            var item = this.getItem(product.id);
            if (item != undefined) {
                item.amount++;
            } else {
                item = {
                    amount: 1,
                    product : product
                }
                items.push(item);
            }
            this.saveInLocalStorage();
        }

        this.increment = function(id, amount) {
            var item = this.getItem(id);
            item.amount = item.amount + amount;
            if (item.amount < 1)
                this.removeProduct(item.product.id);
            this.saveInLocalStorage();
        }

        this.removeProduct = function(id) {
            items = items.filter((item) => 
                item.product.id != id
            )
            this.saveInLocalStorage();
        }
        
        this.getAmount = function(id) {
            var item = this.getItem(id);
            return item.amount;
        }

        this.getItemPrice = function(id) {
            var item = this.getItem(id);
            return item.amount * item.product.price;
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