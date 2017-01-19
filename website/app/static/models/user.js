function User(user) {
    for (var k in user) this[k] = user[k];
    var self = this;
    
    this.wishList = this.wishList.map((product) => new Product(product));
    this.favorites = this.favorites.map((product) => new Product(product));
    this.birthDate = {
        "day" : parseInt(user["birth_date"].split('-')[2]),
        "month" : parseInt(user["birth_date"].split('-')[1]),
        "year" : parseInt(user["birth_date"].split('-')[1]),
    }
    
    this.addWish = (product) => {
        return $.ajax({
                url: "/api/user/wishlist",
                method: 'POST',
                contentType : "application/json",
                data: JSON.stringify({"product_id" : product.id})
        }).then(() => {
            self.wishList.push(product);
            return true;
        });
    }

    this.removeWish = (product) => {
        return $.ajax({
                url: "/api/user/wishlist",
                method: 'DELETE',
                contentType : "application/json",
                data: JSON.stringify({"product_id" : product.id})
        }).then(() => {
            console.log('dix');
            self.wishList = self.wishList.filter((item) => item.id != product.id);
            return false;
        });
    }

    this.addFavorite = (product) => {
        return $.ajax({
            url: "/api/user/favorites",
            method: 'POST',
            contentType : "application/json",
            data: JSON.stringify({"product_id" : product.id})
        }).then(() => {
            self.favorites.push(product);
        });
    }

    this.removeFavorite = (product) => {
        return $.ajax({
            url: "/api/user/favorites",
            method: 'DELETE',
            contentType : "application/json",
            data: JSON.stringify({"product_id" : product.id})
        }).then(() => {
            self.favorites = self.favorites.filter((item) => item.id != product.id);
        });
    }

    this.setWishListPublic = function(bool) {
        return $.ajax({
            url: "/api/user/account",
            method: 'PUT',
            contentType : "application/json",
            data: JSON.stringify({"wishlist_public" : +bool})
        }).then(() => {
            self.wishlist_public = bool;
        });
    }

    this.hasFavorite = function(product) {
        return this.favorites.some((favorite) => favorite.id == product.id);
    }

    this.hasWish = function(product) {
        var x = this.wishList.some((wish) => wish.id == product.id);
        return x;
    }

    this.toJson = function() {
        var obj = {};
        for (var k in user) obj[k] = this[k];
        obj['birth_date'] = this.birthDate;
        return JSON.stringify(obj);
    };

    this.addAddress = function(address) {
        address = JSON.stringify(address);
        return $.ajax({
            url: "/api/user/address",
            type: 'POST',
            contentType : "application/json",
            data: address
        });
    }

    this.removeAddress = function(address) {

    }

    this.updateInfo = function(userInfo) {
        userInfo = JSON.stringify(userInfo);
        return $.ajax({
            url: "/api/user/account",
            method: "PUT",
            contentType : "application/json",
            data: userInfo,
        });
    }

    this.hasBought = function(product) {
        return this.orders.some((order) => order.products.some((boughtProduct) => boughtProduct.id == product.id));
    }
}