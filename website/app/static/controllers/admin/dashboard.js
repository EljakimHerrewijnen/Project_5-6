viewManager.addRoute("/admin/dashboard", () => new adminDashboard());

function adminDashboard() {
    var self = this;
    var container;

    Object.defineProperty(this, "url", {
        get : () => '/admin/dashboard'
    });

    this.construct = function(newContainer) {
        container = newContainer;
        var html = getHtml();
        var users = getUsers()

        promise = Promise.all([html, users]).then(([html, users]) =>{
            html = Handlebars.compile(html);
            container.append(html(users));
            createChart(users);
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
}