function User(user) {
    for (var k in user) this[k] = user[k];
    var self = this;
    
    this.accountType = this.account_type;
    
    this.addWish = (product) => {
        return $.ajax({
                url: "/api/account/wishlist",
                method: 'POST',
                contentType : "application/json",
                data: JSON.stringify({"product_id" : product.id})
        }).then(() => {
            self.wishlist.push(product);
            return true;
        });
    }

    this.removeWish = (product) => {
        return $.ajax({
                url: "/api/account/wishlist",
                method: 'DELETE',
                contentType : "application/json",
                data: JSON.stringify({"product_id" : product.id})
        }).then(() => {
            console.log('dix');
            self.wishlist = self.wishlist.filter((item) => item.id != product.id);
            return false;
        });
    }

    this.addFavorite = (product) => {
        return $.ajax({
            url: "/api/account/favorites",
            method: 'POST',
            contentType : "application/json",
            data: JSON.stringify({"product_id" : product.id})
        }).then(() => {
            self.favorites.push(product);
        });
    }

    this.removeFavorite = (product) => {
        return $.ajax({
            url: "/api/account/favorites",
            method: 'DELETE',
            contentType : "application/json",
            data: JSON.stringify({"product_id" : product.id})
        }).then(() => {
            self.favorites = self.favorites.filter((item) => item.id != product.id);
        });
    }

    this.setwishlistPublic = function(bool) {
        return $.ajax({
            url: "/api/account",
            method: 'PUT',
            contentType : "application/json",
            data: JSON.stringify({"wishlistPublic" : +bool})
        }).then(() => {
            self.wishlist_public = bool;
        });
    }

    this.hasFavorite = function(product) {
        return this.favorites.some((favorite) => favorite.id == product.id);
    }

    this.hasWish = function(product) {
        var x = this.wishlist.some((wish) => wish.id == product.id);
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
            url: "/api/account/address",
            type: 'POST',
            contentType : "application/json",
            data: address
        });
    }

    this.removeAddress = function(address) {

    }

    this.updateInfo = function(userInfo) {
        for (key in userInfo)
            this[key] = userInfo[key]
        userInfo = JSON.stringify(userInfo);
        return $.ajax({
            url: "/api/account/account",
            method: "PUT",
            contentType : "application/json",
            data: userInfo,
        });
    }

    this.hasBought = function(product) {
        return this.orders.some((order) => order.products.some((boughtProduct) => boughtProduct.id == product.id));
    }
}