function Product(id, name, origin, aromas, price, description, roast, image) {
    "use strict"
    var self = this;
    
    this.id = id;
    this.name = name;
    this.origin = origin;
    this.aromas = aromas;
    this.price = parseFloat(price);
    this.description = description;
    this.roast = roast;
    this.image = image;
    this.formatPrice = parseFloat(price).toFixed(2);

    this.matchesFilter = function(filter) {
        var b = true;
        if (filter.name) {
            b = this.hasName(filter.name) && b;
        }
        if(filter.aromas) {
            b = this.hasAroma(filter.aromas) && b;
        }
        if (filter.roasts) {
            console.log("ROAST");
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
    return new Product(
        json.product_id,
        json.name,
        json.origin,
        json.aromas,
        json.price,
        json.description,
        json.roast_level,
        "images/" + json.product_id + ".jpg"
    )
}