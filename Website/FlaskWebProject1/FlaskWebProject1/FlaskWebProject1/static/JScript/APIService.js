var $container = $('#main-container');


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
        if (filter.name != null && filter.name != "") {
            bool = this.hasName(filter.name) && bool;
        }
        if (filter.origin != null && filter.origin != "") {
            bool = this.hasOrigin(filter.origin) && bool;
        }

        if (filter.aromas != null) {
            bool = this.hasAroma(filter.aromas) && bool;
        }
        return bool;
    }

    this.hasName = function(name) {
        return this.productObject.name.toUpperCase().includes(name.toUpperCase());
    }
    
    this.hasPrice = function(min, max) {
        return this.productObject.price >= min && this.productObject.price <= max;
    }

    this.hasAroma = function(aromas) {
        // Need to do due to jquery scoping rules.
        var productObject = this.productObject;
        return aromas.every(function(aroma) {
            return productObject.aromas.includes(aroma);
        });
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
    console.log(products.length);
    products.forEach(function(jsonProduct) {
        finished_html = $(template(jsonProduct));
        $('#main-container').append(finished_html);
        productItems.push(new ProductItem(jsonProduct, finished_html));
    });
    $('#search-button').click(updateFilterSettings);
    $('#search-bar').on('input', updateFilterSettings);
    $('#country-filter').change(updateFilterSettings);
    $('.aroma-box').change(updateFilterSettings);
}

filter = {}

function updateFilterSettings() {
    var searchbar = $('#search-bar');
    var originBox = $('#country-filter');
    var aromas = $('.aroma-box:checked').toArray();
    aromas = aromas.map(function(item) {return item.value });

    filter.name = searchbar.val();
    filter.origin = originBox.val();
    filter.aromas = aromas;
    refreshFilter();
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
        value.htmlObject.remove();
        if (value.matchesFilter(filter)) {
           $('#main-container').append(value.htmlObject);
       }
    });
}

function Product(id, name, origin, aromas, price, description, roast, image) {
    this.id = id;
    this.name = name;
    this.origin = origin;
    this.aromas = aromas;
    this.price = price;
    this.description = description;
    this.roast = roast;
    this.image = image;
    this.htmlObject;

    this.hasName = function(name) {
        return this.name.toUpperCase().includes(name.toUpperCase());
    }
    
    this.hasPrice = function(min, max) {
        return this.price >= min && this.price <= max;
    }

    this.hasAroma = function(aromas) {
        return aromas.every(function(aroma) {
            return this.aromas.includes(aroma);
        });
    }

    this.hasRoast = function(roast) {
        return this.roast == roast;
    }

    this.hasOrigin = function(origin) {
        return this.origin == origin;
    }
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