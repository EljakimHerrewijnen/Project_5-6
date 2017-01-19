function Product(product) {
    for (var k in product) this[k] = product[k];
    "use strict"
    
    var self = this;
    this.id = product.id;
    this.price = parseFloat(this.price);
    this.roast = product.level;
    this.image = "images/" + product.id + ".jpg";
    this.formatPrice = parseFloat(this.price).toFixed(2);

    this.matchesFilter = function(filter) {
        var b = true;
        if (filter.name) {
            b = this.hasName(filter.name) && b;
        }
        if(filter.aromas) {
            b = this.hasAroma(filter.aromas) && b;
        }
        if (filter.roasts) {
            b = this.hasRoast(filter.roasts) && b;
        }
        if (filter.origins) {
            b = this.hasOrigin(filter.origins) && b;
        }
        if (filter.price) {
            b = this.hasPrice(filter.price.min, filter.price.max) && b;
        }
        return b;
    }

    this.hasName = function(name) {
        return this.name.toUpperCase().includes(name.toUpperCase());
    }
    
    this.hasPrice = function(min, max) {
        return this.price >= min && this.price <= max;
    }

    this.hasAroma = function(aromas) {
        return aromas.every(function(aroma) {
            return self.aromas.includes(aroma);
        });
    }

    this.hasRoast = function(roasts) {
        return roasts.includes(self.roast);
    }

    this.hasOrigin = function(origins) {
        return origins.includes(self.origin);
    }
}

function jsonToProduct(json) {
    return new Product(json);
}