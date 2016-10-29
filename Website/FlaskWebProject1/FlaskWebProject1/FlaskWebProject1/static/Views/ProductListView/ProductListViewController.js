
// Global variables.
var products;
var panels;
var viewContainer = $("#view-container");
var filter = {};

// Runs when products & HTML are retrieved.
function onAssetsLoaded() {

    // Create listeners for user interaction.
    $("#search-bar").on("input", updateFilterSettings);
    $("#country-filter").change(updateFilterSettings);
    $(".aroma-box").change(updateFilterSettings);
}

// Reads the filters and updates the filter object.
function updateFilterSettings() {
    var searchbar = $("#search-bar");
    var originBox = $("#country-filter");
    var aromas = $(".aroma-box:checked").toArray();
    aromas = aromas.map(function(item) {return item.value; });

    filter.name = searchbar.val();
    filter.origin = originBox.val();
    filter.aromas = aromas;
    refreshFilter();
}

// Removes all the panels, then adds only the panels that match the filter
function refreshFilter() {
    panels.forEach(function(panel) {
        panel.html.remove();
        if (panel.product.matchesFilter(filter)) {
            $("#products-container").append(panel.html);
        }
    });
}

// Adds the ProductListView.html to the DOM
function buildView(onComplete) {
    return function(){
        ajaxCall("/static/Views/ProductListView/ProductListView.html", "text", {}, function(_view) {
            var view = $(_view);
            viewContainer.append(view);
            onComplete();
        });
    }
}

// Retrieves the Products json and casts them to models.
function buildProducts(onComplete) {
    return function() {
        ajaxCall("/API/Products", "application/json", {}, function(_products){
            products = _products.map( function(product) {
                return new Product(
                    product.id,
                    product.name,
                    product.origin,
                    product.aromas,
                    product.price,
                    product.description,
                    product.roast,
                    product.image
                )
            });
            onComplete();
        });
    }
}

// Retrieves the item panel template.
// Creates panel objects for each product element.
function renderProductPanel(onComplete) {
    return function() {
        ajaxCall("/static/Views/HTML_templates/item_panel.html", "text", {}, function(_productTemplate){
            panels = [];
            _productTemplate = Handlebars.compile(_productTemplate);
            products.forEach(function(product) {
                finished_html = $(_productTemplate(product));
                $("#products-container").append(finished_html);
                panels.push(new Panel(product, finished_html));
            });
            onComplete();
        });
    }
}

// Constructor for panel objects for product element.
function Panel(product, html) {
    this.product = product;
    this.html = html;
}

$(document).ready(function(){   
    var pipeline = buildView(buildProducts(renderProductPanel(onAssetsLoaded)));
    pipeline();
}); 