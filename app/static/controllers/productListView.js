function Panel(product, html) {
    this.product = product;
    this.html = html;
}

viewManager.addRoute("/", () => ProductListView);

var ProductListView = (() => {
    function ProductListView() {
        var self = this;
        var container;
        var products;
        var panels = []
        var filter = {};

        Object.defineProperty(this, "url", {
            get : () => '/'
        });

        addListeners();
        $('#svgitem').load("/static/worldmap.svg");

        this.construct = function(newContainer) {
            container = newContainer;
            var html = self.getHtml();
            var products = stateManager.getProducts();
            var panel = self.getPanel();
            return Promise.all([html, products, panel]).then(([data1, data2, data3]) => {
                container.append(data1);
                var productsContainer = container.find('#products-container');
                productsContainer.addClass('no-opacity');
                $('#svgitem').load("/static/worldmap.svg");
                products = data2;
                panelTemplate = Handlebars.compile(data3);
                products.forEach((product) => {
                    finished_html = $(panelTemplate(product));
                    container.find("#products-container").append(finished_html);
                    panels.push(new Panel(product, finished_html));
                });
            });
        }

        this.destruct = function() {
            var productsContainer = container.find('#products-container');
            var vv = productsContainer.addClass('no-opacity').delay(300).promise().then(() => {container.remove()});
            SideBar.hide();
            return vv;
        }

        this.transitionIn = function() {
            var productsContainer = container.find('#products-container');
            productsContainer.animate({}, 1);
            productsContainer.removeClass('no-opacity');
            SideBar.show();
        }

        this.getHtml = function() {
            return $.ajax({
                url: "/static/views/product-list-view.html",
                contentType: "text"
            });
        }

        this.getPanel = function() {
            return $.ajax({
                url: "/static/views/item-panel.html",
                contentType: "text"
            });
        }

        function addListeners() {
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
            console.log("update");
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
                    container.find("#products-container").append(panel.html);
                }
            });
        }

    }
    return new ProductListView();
})()

function AddProductToCartById(id) {
    var product = stateManager.getProducts
}