var $container = $('#main-container');

var apiService = {
    getProducts : function(callback, arguments) {
        var formatted_arguments;
        for (key in arguments) {
            values = ""
            if (arguments[key] instanceof Array) {
                values = arguments[key].join('+');
            } else {
                values = arguments[key];
            }
            formatted_arguments = formatted_arguments + '&' + key + '=' + values;
        }   
        $.ajax({
            url: "http://localhost:5555/API/Products?" + formatted_arguments,
            contentType: 'application/json',
            datatype: 'json',
        }).done(function(data) {
            callback(data);
        });
    },

    getTemplate : function(url, arguments, callback) {
        $.ajax({
        url: "http://localhost:5555/static/" + url + '?' + arguments,
        datatype: 'text',
        }).done(function(data){
            callback(data);
        });
    }
}

function getTemplate(callback) {
    $.ajax({
        url: "http://localhost:5555/static/item_template.html",
        datatype: 'text',
        }).done(function(data){
            callback(data);
    });
}

var products = []
function renderProductRow(onComplete) {
    var handlebar_template = null;
    function onTemplateRetrieved(template) {
        handlebar_template = Handlebars.compile(template);
        apiService.getProducts(onItemsRetrieved, {'size': 3, 'offset': products.length});   
    }

    function onItemsRetrieved(items) {
        if (items.length < 1) {
            onComplete(true);
        } else {
            var $row = $("<div class='row'></row>")
            $container.append($row);
            for (i in items){
                products.push(items[i])
                $row.append(handlebar_template(items[i]))
            }
            onComplete(false);
        }        
    }
    getTemplate(onTemplateRetrieved)
}

function loadMore() {
    if ($('.loadmore').isOnScreen() === true) {
        renderProductRow(function(isFinished){
            if (!isFinished) {
                loadMore();
            }
        });
    }
}

$(window).scroll(function() {
    loadMore();
});

$(document).ready(function() {
    $container = $('#main-container');
    loadMore();
});