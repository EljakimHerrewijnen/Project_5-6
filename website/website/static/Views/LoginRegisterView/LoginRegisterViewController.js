var viewContainer = $("#view-container");

function buildView() {
    ajaxCall("/static/Views/LoginRegisterView/LoginRegisterView.html", "text", {}, function(_view) {
        var view = $(_view);
        viewContainer.append(view);
        onDone();
    });
}

function login() {

}

function onSuccessfulRegistration() {
    console.log("Created account!")
}

function onFailedRegistration() {
    console.log("Could not make account!")
}



function onDone() {
    $('#register-form').on('submit', function (e) {
        e.preventDefault();
        authenticationService.createUser($("#register-form").serialize());
    });
}

$(document).ready(function() {
    buildView()
});