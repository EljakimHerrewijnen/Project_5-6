function Product(id, name, origin, aromas, price, description, roast, image) {
    "use strict"
    this.id = id;
    this.name = name;
    this.origin = origin;
    this.aromas = aromas;
    this.price = price;
    this.description = description;
    this.roast = roast;
    this.image = image;

    this.matchesFilter = function(filter) {
        var b = true;
        if (filter.name) {
            b = this.hasName(filter.name) && b;
        }
        if(filter.aromas) {
            b = this.hasAroma(filter.aromas) && b;
        }
        if (filter.roast) {
            b = this.hasRoast(filter.roast) && b;
        }
        if (filter.origin) {
            b = this.hasOrigin(filter.origin) && b;
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
        // Scoping in 'every' function overrides 'this'. So we assign the value to a variable.
        var productAromas = this.aromas;
        return aromas.every(function(aroma) {
            return productAromas.includes(aroma);
        });
    }

    this.hasRoast = function(roast) {
        return this.roast == roast;
    }

    this.hasOrigin = function(origin) {
        return this.origin == origin;
    }
}

function jsonToProduct(json) {
    return new Product(
        json.id,
        json.name,
        json.origin,
        json.aromas,
        json.price,
        json.description,
        json.roast,
        json.image
    )
}