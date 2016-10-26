function CallAPI(callback, arguments)
{
    arguments = FormatArguments(arguments);
    _ajaxCall(callback, arguments);

    var product_id = document.head.querySelector("[name=product-id]").content
    console.log(product_id)
}

function _ajaxCall(callback, arguments) {
    return $.ajax({
    url: "http://localhost:5555/API/Products?" + arguments,
    contentType: 'application/json',
    datatype: 'json',
    }).done(function(data) {
        callback(data);
    });
}

function FormatArguments(argument_object)
{
    var formatted_arguments = ""
    for (key in argument_object) {
        values = ""
        if (argument_object[key] instanceof Array) {
            values = argument_object[key].join('+');
        } else {
            values = argument_object[key];
        }
        formatted_arguments = formatted_arguments + '&' + key + '=' + values;
    }
    return formatted_arguments
}

function printData(data){
    console.log(data);
}

function _b(template) {
    var c = function(json) {
        console.log(json);
        html = template(json[0])
        $('#row_1').append(html);
    }

    arguments = {'id': 61}
    CallAPI(c, arguments)
}

function getTemplate(callback) {
    $.ajax({
        url: "http://localhost:5555/static/item_template.html",
        datatype: 'text',
        }).done(function(data){
            callback(data);
    });
}


function renderItems() {
    handlebar_template = null;
    function onTemplateRetrieved(template) {
        handlebar_template = Handlebars.compile(template);
        CallAPI(onItemsRetrieved, {});   
    }

    function onItemsRetrieved(items) {
        row_amount = Math.ceil(items.length / 3);
        var $container = $('#main-container');
        var c = 0
        for (row = 0; row < row_amount; row++) {
            var $row = $("<div class='row'></row>")
            $container.append($row);
            for (i = c; i < c + 3; i++){
                $row.append(handlebar_template(items[i]))
            }
            c++;
        }
    }
    getTemplate(onTemplateRetrieved);
}


function onReady() {
    renderItems();
}

$(window).scroll(function() {
    if($(window).scrollTop() == $(document).height() - 100.0 - $(window).height()) {
           console.log("fire!");
    }
});

$(document).ready(onReady);