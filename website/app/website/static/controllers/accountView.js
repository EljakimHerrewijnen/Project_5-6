var viewContainer = $("#view-container");
viewManager.addRoute("/test/account/", () => new accountView());

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
            if (user.wishlist_public)
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

    this.getHtml = () => $.ajax({url: "http://localhost:5555/static/Views/AccountView/AccountView.html",contentType: "text"});

    this.setupListeners = function(user) {
        var wishlist_toggle = container.find('#wishlist-public-toggle')
        wishlist_toggle.on("change", () => {
            user.setWishListPublic(wishlist_toggle.is(':checked'));
        });
        container.find('#user-address-form').on('submit', this.submitAddressForm(user));
        container.find('#user-info-form').on('submit', this.submitUserInfoForm(user));
    }

    this.submitAddressForm = (user) => function(e) {
        e.preventDefault();
        var values = {};
        container.find("#user-address-form").serializeArray().map( function(field) {
            values[field.name] = field.value;
        });
        user.addAddress(values).then(() => {
            var table = container.find('#account-address-container tbody')[0];
            var row = table.insertRow(1);
            var i = 0;
            for (var k in values) {
                var cell = row.insertCell(i);
                cell.innerHTML = values[k];
                i = i + 1;
            }
            var cell = row.insertCell(i);
            cell.innerHTML = `<a onclick='removeAddress("${values.postal_code}", ${values.house_number}, this)'>Delete</a>`
        });
    }

    this.submitUserInfoForm = (user) => function(e) {
        e.preventDefault();
        var formValues = {};
        container.find('#user-info-form').serializeArray().map( function(field) {
            formValues[field.name] = field.value;
        });
        var updatedUser = {};
        updatedUser["name"] = formValues.name;
        updatedUser["surname"] = formValues.surname;
        updatedUser["birth_date"] = {
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

function removeAddress(postal_code, house_number, button) {
    var row = button.closest('tr');
    values = JSON.stringify({
        "postal_code" : postal_code,
        "house_number" : house_number
    });
    $.ajax({
        url: "/api/user/address",
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