function formatArguments(arguments)
{
    var formatted_arguments = "";
    for (key in arguments) {
        values = ""
        if (arguments[key] instanceof Array) {
            values = arguments[key].join('+');
        } else {
            values = arguments[key];
        }
        formatted_arguments = formatted_arguments + '&' + key + '=' + values;
    }
    return formatted_arguments;
}

function ajaxCall(path, contentType, arguments, resultHandler) {
    arguments = formatArguments(arguments);
    $.ajax({
        url: "http://localhost:5555" + path + "?" + arguments,
        contentType: contentType
    }).done(function(data) {
        resultHandler(data);
    });
}

var getProducts = function(args, resultHandler){
    ajaxCall("/API/Products", "application-json", args, resultHandler);
}

var addToContainer = function(final_html) {
    $('#main-container').append(final_html)
}

var getTemplate = function(args, path, resultHandler) {
    ajaxCall("/static/" + path, "text", args, resultHandler);
}