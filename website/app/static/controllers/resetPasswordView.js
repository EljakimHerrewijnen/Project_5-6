viewManager.addRoute('/reset-password/(.)+', (path) => {
    var hash = path.split('/').pop();
    return new ResetPasswordField(hash);
});

function ResetPasswordField(hash) {
    var self = this;
    var container;
    console.log("im here");

    Object.defineProperty(this, "url", {
        get : () => '/reset-password/' + hash
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

    this.getHtml = () => $.ajax({url: "/static/views/reset-password-view.html",contentType: "text"});

    var resetPassword = function(e) {
        e.preventDefault();
        var passwordForm = container.find('#user-password-reset-form');
        var payload = {};
        var d = passwordForm.serializeArray()
        console.log(d);
        d.map((x) => payload[x.name] = x.value);
        console.log(payload)
        payload['hash'] = hash
        $.post({url: "/api/password-reset",contentType: "application/json", data: JSON.stringify(payload)});
    }

    attachListeners = function() {
        var passwordForm = container.find('#user-password-reset-form');
        passwordForm.submit(resetPassword);
    }    
}