var viewContainer = $("#view-container");
var registrationForm;
var loginForm;

function buildView() {
    ajaxCall("/static/Views/LoginRegisterView/LoginRegisterView.html", "text", {}, function(_view) {
        var view = $(_view);
        viewContainer.append(view);
        onViewLoad();
    });
}

function onSuccessfulRegistration() {
    $('#register-error-box').text("success!");
}

function onFailedRegistration(jqXHR, textStatus, errorThrown) {
    $('#register-error-box').text(jqXHR.responseText);
}

function onViewLoad() {
    $('#register-form').on('submit', function (e) {
        e.preventDefault();
        if (validateRegistrationForm())
        {
            authenticationService.createUser($("#register-form").serialize(),onSuccessfulRegistration, onFailedRegistration);
        }
    });


    $('#login-form').on('submit', function(e) {
        e.preventDefault();
        if (validateLoginForm())
        {
            var username = $('#login-form input[name=username]').val();
            var password = $('#login-form input[name=password]').val()
            authenticationService.attemptLogin(username, password, onSuccessfulRegistration, onFailedRegistration);
        }
    });
}

$(document).ready(function() {
    buildView()
});

function failedLogin() {
    $('#register-error-box').text("Failed to log in!");
}

function successLogin() {
    $('#register-error-box').text("Logged in!");
}

function validateLoginForm() {
    var x = $("#register-error-box").text("");

    var rules = {
        password : {required: true},
        username : {required: true}
    }

    var errorMessages = {
        password : "Please enter a password",
        username : "Please enter a username"
    }

    return ValidateForm($("#login-form"), rules, errorMessages, x);
}

function validateRegistrationForm() {
    $("#register-error-box").text("");

    var rules = {
        username : { required: true},
        email : { required: true, email: true},
        password : {minLength: 5},
        password_verify : {validates: "password"},
        name: {required: true},
        surname: {required: true},
        postal_code: {minLength: 6, maxLength: 6, required: true},
        number: {required: true},
        year: {required: true},
        month: {required: true},
        day: {required: true}
    }

    var errorMessages = {
        username : "Please fill in a username",
        email : "Email is invalid!",
        password: "Password is not long enough!",
        password_verify: "Passwords do not match!",
        name: "Please enter your first name",
        surname: "Please enter your surname",
        postal_code: "The postal code is incorrect!",
        number: "Please enter a street number!",
        year: "Please enter you date of birth!",
        month: "Please enter you date of birth!",
        day: "Please enter you date of birth!"
    }

    return ValidateForm($('#register-form'), rules, errorMessages, $("#register-error-box"));
}

function ValidateForm(form, rules, failureMessages, errorField)
{
    for (name in rules)
    {
        var isValid = true;
        var element = form.find("input[name=" + name + "]");

        if (rules[name].required) {
            if (element.val() == "") isValid = false;
        }
        if (rules[name].email) {
            if (!element.get(0).validity.valid) isValid = false;
        }

        if (rules[name].minLength) {
            if (element.val().length < rules[name].minLength) isValid = false;
        }

        if(rules[name].maxLength) {
            if (element.val().length > rules[name].maxLength) isValid = false;
        }

        if (rules[name].validates) {
            var validateElement = form.find("input[name=" + rules[name].validates + "]");
            var x = element.val();
            var y = validateElement.val();
            if (!(element.val() == validateElement.val())) {
                isValid = false;
            }
        }

        if (!isValid) {
            errorField.text(failureMessages[name]);
            return false;
        }
    }
    return true;
}