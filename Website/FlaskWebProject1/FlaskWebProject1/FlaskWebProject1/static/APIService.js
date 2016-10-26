function CallAPI(callback, arguments)
{
    arguments = FormatArguments(arguments);
    _ajaxCall(callback, arguments);
}

function _ajaxCall(callback, arguments) {
    return $.ajax({
    url: "http://localhost:5555/API/Products?" + arguments,
    contentType: 'application/json',
    datatype: 'text json'
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
arguments = {
    "Name": "Velton",
    "Max": 15,
    "Min": 10
}

CallAPI(printData, arguments);