var viewContainer = $("#view-container");

function userCallback(x) {
    user = x;
    buildView();
}

function buildView() {
    if (user == undefined){
        //window.location.replace("http://localhost:5555/login")
        return;
    }

    ajaxCall("/static/Views/AccountView/AccountView.html", "text", {}, function(_view) {
        var view = Handlebars.compile(_view);
        user["birth_date"] = dateFromTimestamp(user["birth_date"]);
        viewContainer.append(view(user));
        onViewLoad();
    });
}

$(document).ready(function() {
    authenticationService.getUser(userCallback);
});

function onViewLoad() {
    $('#logout-button').click(function(e){
        authenticationService.logout();
    })
    $('#user-info-form').on('submit', function(e){
        e.preventDefault();
        var formValues = {};
        $("#user-info-form").serializeArray().map( function(field) {
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
        var jsonValues = JSON.stringify(updatedUser);
        authenticationService.updateUser(jsonValues,onUpdate, onFailedUpdate);
    });

    $('#user-address-form').on('submit', function(e){
        e.preventDefault();
        var values = {};
        $("#user-address-form").serializeArray().map( function(field) {
            values[field.name] = field.value;
        });
        values = JSON.stringify(values);
        $.ajax({
            url: "/api/user/address",
            method: "POST",
            contentType : "application/json",
            data: values,
            success: onAddressAdded,
            error: onFailedAddressAdd
        })
    });
}


function onAddressAdded() {
    location.reload();
}

function onFailedAddressAdd(jqXHR, textStatus, errorThrown) {
    alert("Could not add address: " + jqXHR.responseText);
}

function onUpdate() {
    alert("Updated user information");
    location.reload();
}

function onFailedUpdate() {
    alert("Failed to update usert information");
}

function dateFromTimestamp(timestamp) {
    var spl = timestamp.split('-');
    return {
        "day" : parseInt(spl[2]),
        "month" : parseInt(spl[1]),
        "year" : parseInt(spl[0])
    }
}

function removeAddress(postal_code, house_number) {
    values = JSON.stringify({
        "postal_code" : postal_code,
        "house_number" : house_number
    });
    $.ajax({
        url: "/api/user/address",
        method: "DELETE",
        contentType : "application/json",
        data: values,
        success: onAddressAdded,
        error: function(e) {alert(e)}
    })
}

