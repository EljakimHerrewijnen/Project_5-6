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
    alert("Created your account")
}

function onFailedRegistration(jqXHR, textStatus, errorThrown) {
    alert("Failed to creae accounts: " + jqXHR.responseText)
}

function onViewLoad() {
    $('#register-form').on('submit', function (e) {
        e.preventDefault();

        var formValues = {}
        $("#register-form").serializeArray().map( function(field) {
            formValues[field.name] = field.value;
        });
        console.log(formValues)
        jsonValues = {}
        jsonValues["username"] = formValues.username
        jsonValues["password"] = formValues.password
        jsonValues["name"] = formValues.name
        jsonValues["surname"] = formValues.surname
        jsonValues["birth_date"] = {
            day : formValues.day,
            month : formValues.month,
            year : formValues.year
        }
        jsonValues["email"] = formValues.email
        jsonValues = JSON.stringify(jsonValues)
        console.log(jsonValues)
        authenticationService.createUser(jsonValues,onSuccessfulRegistration, onFailedRegistration);
    });


    $('#login-form').on('submit', function(e) {
        e.preventDefault();
        if (validateLoginForm())
        {
            var username = $('#login-form input[name=username]').val();
            var password = $('#login-form input[name=password]').val()
            authenticationService.attemptLogin(username, password, successLogin, failedLogin);
        }
    });
}

$(document).ready(function() {
    buildView();
});

function failedLogin() {
    alert("Failed to log in")
}

function successLogin() {
    window.location.replace("http://localhost:5555/account")
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