
// Global variables.
var products;
var panels;
var viewContainer = $("#view-container");
var filter = {};


async function loadStory(){
    return "";
}

// Runs when products & HTML are retrieved.
function onAssetsLoaded() {
    // Create listeners for user interaction.
    $("#search-bar").on("input", updateFilterSettings);
    $("#country-filter").change(updateFilterSettings);
    $(".aroma-box").change(updateFilterSettings);
    $('.origin-box').change(updateFilterSettings);
    $('.roast-box').change(updateFilterSettings);
    $('#price-range').on("input", updateSlider);
    $('#price-range').change(updateFilterSettings);
}

function updateSlider() {
    var value = $('#price-range').val();
    $("#price-indicator").html("€" + value);
}

// Updates the map
function updateMap(maps) {
    $('#Americas').attr("fill", "#C4C4C4");
    $('#Americas').attr("stroke", "#C4C4C4");
    $('#Africa').attr("fill", "#C4C4C4");
    $('#Africa').attr("stroke", "#C4C4C4");
    $('#Asia').attr("fill", "#C4C4C4");
    $('#Asia').attr("stroke", "#C4C4C4");

    maps.forEach(function(item){
        if (item == "Africa"){
            $('#Africa').attr("fill", "#4688F1");
            $('#Africa').attr("stroke", "#4688F1");
        } else if (item == "Americas") {
            $('#Americas').attr("fill", "#FF5151");
            $('#Americas').attr("stroke", "#FF5151");
        } else if (item == "Asia") {
            $('#Asia').attr("fill", "#FABC2D");
            $('#Asia').attr("stroke", "#FABC2D");
        }
    });
}

// Reads the filters and updates the filter object.
function updateFilterSettings() {
    var searchbar = $("#search-bar");
    var priceSlider = $("#price-range");
    var originBox = $("#country-filter");
    var aromas = $(".aroma-box:checked").toArray();
    var origins = $('.origin-box:checked').toArray();
    var roasts = $('.roast-box:checked').toArray();
    aromas = aromas.map(function(item) {return item.value; });
    origins = origins.map(function(item) {return item.value; })
    roasts = roasts.map(function(item) {return item.value; })
    updateMap(origins);

    filter.name = searchbar.val();
    filter.aromas = aromas;
    filter.origins = origins;
    filter.roasts = roasts;
    filter.price = {max: priceSlider.val(), min: 0};
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
            $('#svgitem').load("/static/worldmap.svg");
            onComplete();
        });
    }
}

// Retrieves the Products json and casts them to models.
function buildProducts(onComplete) {
    return function() {
        ajaxCall("/API/Products", "application/json", {}, function(_products){
            products = _products.map( function(product) {
                return jsonToProduct(product);
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

