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
                var forms = container.find('form');
                forms.each((x) => {
                    stateManager.addRealtimeVerify(forms[x]);
                });
            })
            return Promise.resolve(html);
        }
        
        this.destruct = function() {
            return container.animate({opacity: 0}, 150).promise().then(() => container.remove());
        }

        this.transitionIn = function() {
            container.animate({opacity: 1}, 150);
        }

        this.getHtml = () => $.ajax({url: "/static/views/login-view.html",contentType: "text"});

        var register = function(form) {
            values = {}
            var errorBox = container.find('#register-error-box');
            if(!stateManager.submitVerify(form)) {
                return;
            };

            var form = form.serializeArray().map((field) => values[field.name] = field.value);
            values["birthDate"] = {
                day : values["day"],
                month : values["month"],
                year : values["year"]
            }
            delete values["day"];
            delete values["month"];
            delete values["year"];
            response = auth.createUser(values);
            response.then((success) => {
                alert("Created your account")
                auth.login(values['username'], values['password']).then((success) => {
                    viewManager.changeView(new accountView());
                });
            }, (jqXHR) => {
                var errorBox = container.find('#register-error-box');
                errorBox.html("Failed to create your account: " + jqXHR.responseText)
            });
        }

        var login = function(form) {
            var errorBox = container.find('#login-error-box');
            if (!stateManager.submitVerify(form)) {
                return;
            };
            var username = form.find('input[name=username]').val();
            var password = form.find('input[name=password]').val();
            response = auth.login(username, password);
            response.then((success) => {
                viewManager.changeView(new accountView());
            }, (jqXHR) => {
                var errorBox = container.find('#login-error-box');
                errorBox.html("Failed to login: " + jqXHR.responseText)
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