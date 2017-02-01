viewManager.addRoute("/admin/dashboard", () => new adminDashboard());

function adminDashboard() {
    var self = this;
    var container;
    var options = {
        responsive: true,
        maintainAspectRatio: false
    };
    var selectedUser;
    var allUsers;

    Object.defineProperty(this, "url", {
        get : () => '/admin/dashboard'
    });

    this.construct = function(newContainer) {
        container = newContainer;
        var html = getHtml();
        var users = getUsers();
        var products = stateManager.getProducts();

        promise = Promise.all([html, users, products]).then(([html, users, products]) => {
            allUsers = users.filter((u) => u.accountType != "admin");
            html = Handlebars.compile(html);
            container.append(html(allUsers));
            createChart(allUsers);
            createProductChart(products);
            createAromaChart(products);
            setupUserTable();
            container.css({opacity: 0});
        });
        return promise;
    }

    this.destruct = function() {
        return container.animate({opacity:0}, 150).promise().then(() => container.remove());
    }

    this.transitionIn =function() {
        container.animate({opacity: 1}, 150);
    }
    
    var getHtml = () => $.ajax({url: "/static/views/admin/dashboard.html"});
    var getUsers = () => $.ajax({url: "/api/admin/account"});

    var createChart = (users) => {
        Chart.defaults.global.legend.display = false;
        var options = {
            responsive: true,
            maintainAspectRatio: false
        };
        var data = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        users.forEach((x) => {
            data[x.birthDate.month - 1]++;
        });


        var data = {
            labels: ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"],
            datasets: [
                {
                    backgroundColor: "rgba(0,0,0,0)",
                    borderColor: "#00bfc7",
                    data: data
                },
            ]
        };

        var ctx = container.find("#orderChart");
        var myLineChart = new Chart(ctx, {
            type: 'line',
            data: data,
            options: options
        });
    }

    var createProductChart = function(products) {
        Chart.defaults.global.legend.display = true;
        var darkAmount = products.filter((x) => x.roast == "Dark").length;
        var mediumAmount = products.filter((x) => x.roast == "Medium").length;
        var lightAmount = products.filter((x) => x.roast == "Light").length;

        var data = {
            labels: [
                "Dark",
                "Medium",
                "Light"
            ],
            datasets: [
                {
                    data: [darkAmount, mediumAmount, lightAmount],
                    backgroundColor: [
                        "#FF6384",
                        "#36A2EB",
                        "#FFCE56"
                    ],
                    hoverBackgroundColor: [
                        "#FF6384",
                        "#36A2EB",
                        "#FFCE56"
                    ]
                }]
        };

        var ctx = container.find("#productChart");
        var myDoughnutChart = new Chart(ctx, {
            type: 'doughnut',
            data: data,
            options: options,
            animation:{
                animateScale:true
            }
        });
    }

    var createAromaChart = function(products) {
        Chart.defaults.global.legend.display = true;
        var chocolate = products.filter((x) => $.inArray("Chocolate", x.aromas)).length;
        var nutty = products.filter((x) => $.inArray("Nutty", x.aromas)).length;
        var fruity = products.filter((x) => $.inArray("Fruity", x.aromas)).length;
        var spicy = products.filter((x) => $.inArray("Spicy", x.aromas)).length;

        var data = {
            labels: [
                "Chocolate",
                "Nutty",
                "Spicy",
                "Fruity"
            ],
            datasets: [
                {
                    data: [chocolate, nutty, spicy, fruity],
                    backgroundColor: [
                        "#FF6384",
                        "#4BC0C0",
                        "#FFCE56",
                        "#36A2EB"
                    ]
            }]
        }

        var ctx = container.find("#aromaChart");
        new Chart(ctx, {
            data: data,
            type: 'polarArea',
            options: options
        });
    }

    var setupUserTable = function() {
        var rows = container.find('.admin-user-row');
        rows.each(function(row) {
            $(this).on("click", activateEditor);
        });
        var form = container.find('#admin-user-form');
        form.submit(submitForm);   
    }

    var toggleDisabled = function() {
        $(this).removeClass('disabled')
        $(this).prop('disabled', false)
    }

    var activateEditor = function(e) {
        var form = container.find('#admin-user-form');
        var inputFields = form.find('input');
        var buttons = form.find('button');
        var labels = form.find('label');
        inputFields.each(toggleDisabled);
        buttons.each(toggleDisabled);
        labels.each(toggleDisabled);
        var username = $(this).attr('user');
        var user = allUsers.find((user) => user.username == username);
        fillForm(form, user);
        fillForm(form, user.birthDate);
        setupBanButton(user);
        setupPasswordResetButton(user);
    }

    var fillForm = function(form, values) {
        for (key in values) {
            var field = form.find('[name=' + key + ']');
            if (field)
                field.val(values[key])
        }
    }

    var setupBanButton = function(user) {
        var btn = container.find('#ban-user');
        btn.attr("username", user.username)
        btn.off("click");
        btn.click(toggleBan);
       if (+user.banned) {
            btn.html("Unban user");
        } else {
            btn.html("Ban user");
        }
    }

    var setupPasswordResetButton = function(user) {
        var xxx = container.find('#reset-password');
        xxx.off("click");
        xxx.click(function(e) {
            e.preventDefault();
            $.post({
                url: "/api/request-password-reset",
                contentType: "application/json",
                data: JSON.stringify({email: user.email})
            }).then((a, b, c) => {
                alert("Password change is sent");
                console.log(a);
                console.log(b);
                console.log(c);
            }, (jqXHR) => {
                alert("Failed to modify password: " + jqXHR.responseText);
                var errorBox = container.find('#user-error-box');
                errorBox.html("Failed to modify password: " + jqXHR.responseText)
            });
        })
    }

    var toggleBan = function(e) {
        e.preventDefault()
        var username = $(this).attr('username');
        var user = allUsers.find((user) => user.username == username);
        var json = {"banned" : 1, "username" : username};
        if (user.banned) {
            json.banned = 0;
        }
        updateUser(json).then((u) => {
            user.banned = -!+user.banned
            setupBanButton(user);
        });
    }

    var submitForm = function(e) {
        e.preventDefault();
        var values = {}
        $(this).serializeArray().forEach((v) => values[v.name] = v.value);
        var user = allUsers.find((user) => user.username == values.username)
        for (key in values) {
            user[key] = values[key]
        }
        user['birthDate'] = {
            day : values.day,
            month : values.month,
            year: values.year
        }
        delete user['year']
        delete user['month']
        delete user['day']
        updateUser(user);
        var z = container.find('[user=' + user.username + ']').children().get(1);
        $(z).html(user.name + " " + user.surname);
        stateManager.getUser().then((u) => {
            if (u.username === user.username)
                stateManager.clearUser();
        });
    }

    var formatUser = function(userInfo) {
        return userInfo
    }

    var updateUser = function(userInfo) {
        var payload = formatUser(userInfo);
        return $.ajax({
            url: "/api/admin/account/" + userInfo.username,
            method: "PUT",
            contentType : "application/json",
            data: JSON.stringify(payload),
        });
    }
}