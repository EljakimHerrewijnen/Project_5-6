var $container = $('#main-container');
var filtersettings = {
}

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

function ajaxCall(resultHandler) {
    return function(state) {
        return function(path, contentType, arguments) {
            arguments = formatArguments(arguments);
            $.ajax({
                url: "http://localhost:5555" + path + "?" + arguments,
                contentType: contentType
            }).done(function(data) {
                state.push(data);
                resultHandler(state);
            });
        }
    }
}

function ajaxCall2(path, contentType, arguments, resultHandler) {
    arguments = formatArguments;
    $.ajax({
        url: "http://localhost:5555" + path + "?" + arguments,
        contentType: contentType
    }).done(function(data) {
        resultHandler(data);
    });
}


var getProducts = function(args){
    return function(continuation) {
        return function(state) {
            ajaxCall(continuation)(state)("/API/Products", "application-json", args);
        }
    }
}

var addToContainer = function(final_html) {
    $('#main-container').append(final_html)
    this.element = final_html;
}

var getTemplate = function(args, path) {
    return function(continuation) {
        return function(state) {
            ajaxCall(continuation)(state)("/static/" + path, "text", args);
        }
    }   
}

function ProductRowRenderer() {
    var renderRow = function(continuation) {
        return function(state) {
            row = $("<div class'row'></div>");
            html = state[1];
            items = state[0];
            template = Handlebars.compile(html);
            for (i = 0; i < items.length; i++){
                row.append(template(items[i]));
            }
            continuation(row);
        }
    }

    productArguments = filtersettings;

    this.addRowIfItemsLeft = function() {
        var productGetter = getProducts(productArguments);
        var templateGetter = getTemplate({"a": "b"}, "item_template.html")

        var pipeline = productGetter(templateGetter(renderRow(addToContainer)));
        pipeline([]);
    }

    this.hasItemsLeft = function(){
        return !reachedEnd;
    }

    this.resetRows = function() {
        $container.html.clear();
        offset = 0;
        items = [];
    }
}

function ProductItem(object, html) {
    this.productObject = object;
    this.htmlObject = html;

    this.matchesFilter = function(filter) {
        var bool = true;
        if (filter.name != null) {
            bool = this.hasName(filter.name) && bool;
        }
        if (filter.origin != null) {
            bool = this.hasOrigin(filter.origin) && bool;
        }
        return bool;
    }

    this.hasName = function(name) {
        return this.productObject.name.includes(name);
    }
    
    this.hasPrice = function(min, max) {
        return this.productObject.price >= min && this.productObject.price <= max;
    }

    this.hasOrigin = function(origin) {
        return this.productObject.origin == origin;
    }
}

function ProductWindow() {
    this.products = [];
    var productRenderer = new ProductRowRenderer();
    productRenderer.addRowIfItemsLeft();
}

var products = []
var productItems = []
var productTemplate;

function onDataReady() {
    template = Handlebars.compile(productTemplate);
    products = products.concat(products.concat(products.concat(products.concat(products.concat(products.concat(products))))));
    products = products.concat(products);
    console.log(products.length);
    products.forEach(function(jsonProduct) {
        finished_html = $(template(jsonProduct));
        $('#main-container').append(finished_html);
        productItems.push(new ProductItem(jsonProduct, finished_html));
    });
    $('#search-button').click(refreshFilter);
}

filter = {
    'name' : '49'
}

function updateFilterSettings() {
    
}

function matchFilter(product, filter)
{
    var bool = true;
    for (key in filter) {
        bool = filter[key] == product[key] && bool
    }
    return bool;
}


function refreshFilter() {
    productItems.forEach(function(value) {
        console.log('hi');
        value.htmlObject.remove();
        if (value.matchesFilter(filter)) {
           $('#main-container').append(value.htmlObject);
       }
    });
}



$(document).ready(function(){
    ajaxCall2("/API/Products", 'application/json', {}, function(result){
        products = result;
        ajaxCall2('/static/item_template.html', 'text', {}, function(result){
            productTemplate = result;
            onDataReady();
        });
    })
});