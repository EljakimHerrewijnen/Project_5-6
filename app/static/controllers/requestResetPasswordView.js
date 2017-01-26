viewManager.addRoute('/request-reset-password', () => new RequestResetPassword());

function RequestResetPassword() {
    var self = this;
    var container

    Object.defineProperty(this, "url", {
        get : () => '/request-reset-password'
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

    this.getHtml = () => $.ajax({url: "/static/views/request-password-reset-view.html",contentType: "text"});

    var resetPassword = function(e) {
        e.preventDefault();
        var passwordForm = container.find('#request-password-reset-form');
        var errorBox = container.find('#error-box');
        var payload = {};
        var d = passwordForm.serializeArray()
        d.map((x) => payload[x.name] = x.value);
        var promise = $.post({url: "/api/request-password-reset",contentType: "application/json", data: JSON.stringify(payload)});
        promise.then((done) => {
            alert(done);
            viewManager.redirect("/login");
        }, (error) => {
            console.log(error.responseText);
            errorBox.html(error.responseText);
            errorBox.removeClass("hidden");
        });
    }

    attachListeners = function() {
        var passwordForm = container.find('#request-password-reset-form');
        passwordForm.submit(resetPassword);
    }    
}