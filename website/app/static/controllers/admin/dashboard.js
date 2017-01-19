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
        var users = getUsers()
        var products = stateManager.getProducts();

        promise = Promise.all([html, users, products]).then(([html, users, products]) => {
            allUsers = users;
            html = Handlebars.compile(html);
            container.append(html(users));
            createChart(users);
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

        var data = {
            labels: ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dev"],
            datasets: [
                {
                    backgroundColor: "rgba(0,0,0,0)",
                    borderColor: "#00bfc7",
                    data: [52, 66, 40, 29, 50, 75, 67, 38, 55, 77, 66, 39]
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
        form.submit(updateUser);
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
        var user = new User(allUsers.find((user) => user.username == username));
        fillForm(form, user);
        fillForm(form, user.birthDate);
    }

    var fillForm = function(form, values) {
        for (key in values) {
            var field = form.find('[name=' + key + ']');
            if (field)
                field.val(values[key])
        }
    }

    var updateUser = function(e) {
        e.preventDefault();
        var x = {};
        $(this).serializeArray().forEach((v) => x[v.name] = v.value);
        x['birthDate'] = {
            day: x.day,
            month: x.month,
            year: x.year
        }
    }
}