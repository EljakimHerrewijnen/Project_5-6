var viewContainer = $("#view-container");
viewManager.addRoute("/account", () => new accountView());

function accountView() {
    var self = this;
    var container;

    Object.defineProperty(this, "url", {
        get : () => '/account'
    });
    
    this.construct = function(newContainer) {
        container = newContainer;
        html = this.getHtml();
        user = stateManager.getUser();

        promise = Promise.all([html, user]).then(function([html, user]) {
            container.css({opacity: 0});
            html = Handlebars.compile(html);
            html = html(user);
            container.append(html);
            if (user.wishlistPublic)
                container.find('#wishlist-public-toggle').prop("checked", true);
            self.setupListeners(user);
        });
        return promise;
    }
    
    this.destruct = function() {
        return container.animate({opacity: 0}, 150).promise().then(() => {container.remove()});
    }

    this.transitionIn = function() {
        container.animate({opacity: 1}, 150);
    }

    this.getHtml = () => $.ajax({url: "/static/views/account-view.html",contentType: "text"});

    this.setupListeners = function(user) {
        var wishlist_toggle = container.find('#wishlist-public-toggle')
        wishlist_toggle.on("change", () => {
            user.setwishlistPublic(wishlist_toggle.is(':checked'));
        });
        stateManager.addRealtimeVerify(container.find('#user-address-form'));
        container.find('#user-address-form').on('submit', this.submitAddressForm(user));
        container.find('#user-info-form').on('submit', this.submitUserInfoForm(user));
    }

    this.submitAddressForm = (user) => function(e) {
        e.preventDefault();
        var values = {};
        var form = container.find('#user-address-form');
        if (!stateManager.submitVerify(form)) {
            return;
        };
        form.serializeArray().map( function(field) {
            values[field.name] = field.value;
        });

        user.addAddress(values).then(() => {
            var table = container.find('#account-address-container tbody')[0];
            var row = table.insertRow(1);
            var cell = row.insertCell(0);
            cell.addClass('big-only');
            cell.innerHTML = values['country']
            var cell = row.insertCell(1);
            cell.addClass('big-only');
            cell.innerHTML = values['city']
            var cell = row.insertCell(2);
            cell.innerHTML = values['street']
            var cell = row.insertCell(3);
            cell.innerHTML = values['houseNumber']
            var cell = row.insertCell(4);
            cell.innerHTML = values['postalCode']
            var cell = row.insertCell(5);
            cell.innerHTML = `<a onclick='removeAddress("${values.postal_code}", ${values.house_number}, this)'>Delete</a>`
        });
    }

    this.submitUserInfoForm = (user) => function(e) {
        e.preventDefault();
        var formValues = {};
        var form = container.find('#user-info-form');
        if (!stateManager.submitVerify(form)) {
            return;
        };

        form.serializeArray().map( function(field) {
            formValues[field.name] = field.value;
        });
        var updatedUser = {};
        updatedUser["name"] = formValues.name;
        updatedUser["surname"] = formValues.surname;
        updatedUser["birthDate"] = {
            day : formValues.day,
            month : formValues.month,
            year : formValues.year
        };
        updatedUser["email"] = formValues.email;
        user.updateInfo(updatedUser).then(() => {
            console.log("Updated info");
        }, (error) => {
            alert("Failed to update user info");
            console.log(error);
        });
    }
}

function removeAddress(postalCode, houseNumber, button) {
    var row = button.closest('tr');
    values = JSON.stringify({
        "postalCode" : postalCode,
        "houseNumber" : houseNumber
    });
    $.ajax({
        url: "/api/account/address",
        method: "DELETE",
        contentType : "application/json",
        data: values
    }).then(() => {
        row.remove();
    });
}

function removeWishItem(id, button) {
    var row = button.closest('tr');
    var user = stateManager.getUser();
    user.then((user) => {
        user.removeWish({id : id});
    }).then(() => {
        row.remove();
    });
}

function removeFavoriteItem(id, button) {
    var row = button.closest('tr');
    var user = stateManager.getUser();
    user.then((user) => {
        user.removeFavorite({id : id});
    }).then(() => {
        row.remove();
    });
}