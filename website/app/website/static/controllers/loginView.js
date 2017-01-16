var viewContainer = $("#view-container");
var registrationForm;
var loginForm;

viewManager.addRoute("/login", () => loginRegisterView);

var loginRegisterView = (() => {
    function loginRegisterView() {
        var self = this;
        var container;
        var attachListeners;

        Object.defineProperty(this, "url", {
            get : () => '/login'
        });

        this.construct = function(newContainer) {
            container = newContainer;
            html = this.getHtml();
            html.then((html) => {
                container.css({opacity: 0})
                container.append(html);
                attachListeners();
            })
            return Promise.resolve(html);
        }
        
        this.destruct = function() {
            return container.animate({opacity: 0}, 150).promise().then(() => container.remove());
        }

        this.transitionIn = function() {
            container.animate({opacity: 1}, 150);
        }

        this.getHtml = () => $.ajax({url: "http://localhost:5555/static/views/login-view.html",contentType: "text"});

        var register = function(form) {
            values = {}
            var form = form.serializeArray().map((field) => values[field.name] = field.value);
            values["birth_date"] = {
                day : values["day"],
                month : values["month"],
                year : values["year"]
            }
            delete values["day"];
            delete values["month"];
            delete values["year"];
            delete values["password_verify"];
            response = auth.createUser(values);
            response.then((success) => {
                alert("Created your account")
            }, (failure) => {
                alert("Failed to create your account: " + jqXHR.responseText)
            });
        }

        var login = function(form) {
            var username = form.find('input[name=username]').val();
            var password = form.find('input[name=password]').val();
            response = auth.login(username, password);
            response.then((success) => {
                viewManager.changeView(new accountView());
            }, (failure) => {
                alert("Incorrect username or password");
            });
        }

        attachListeners = function() {
            var registrationForm = container.find('#register-form');
            var loginForm = container.find('#login-form');
            
            registrationForm.on('submit', (e) => {e.preventDefault(); register(registrationForm)});
            loginForm.on('submit', (e) => {e.preventDefault(); login(loginForm)});
        }    
    }
    return new loginRegisterView()
})();

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