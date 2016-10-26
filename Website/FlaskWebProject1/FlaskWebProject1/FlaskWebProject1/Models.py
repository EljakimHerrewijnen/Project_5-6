import json

class Product:
    def __init__(self, id, name, description, price, roast, origin, aromas, image):
        self.id = id
        self.name = name
        self.description = description
        self.price = price
        self.roast = roast
        self.origin = origin
        self.aromas = aromas
        self.image = image

    @staticmethod
    def _fromJson(jsonFile):
        return Product(
            jsonFile["ID"],
            jsonFile["Name"],
            jsonFile["Description"],
            float(jsonFile["Price"]),
            jsonFile["Roast"],
            jsonFile["Origin"],
            jsonFile["Aromas"],
            jsonFile["Image"]
        )

    def description_contains(self, expression):
        return expression in self.description

    def has_aromas(self, aromas, match_all = False):
        if (match_all):
            return set(aromas) == set(self.aromas)
        for aroma in aromas:
            if aroma in self.aromas:
                return True
        return False
    
    def has_price(self, min = 0, max = 100):
        return min <= self.price <= max

    def has_name(self, name, partial_match = True):
        if (partial_match):
            return name in self.name
        return name == self.name

    def has_origin(self, origin):
        return self.origin == origin
        
    def has_roast(self, roast):
        return self.roast == roast

    @staticmethod
    def get_all():
        data = open("FlaskWebProject1/products.json", 'r')
        jsonData = json.load(data)
        
        products = []
        for item in jsonData:
            products.append(Product._fromJson(item))
        return products
        
    def __dict__(self):
        result = { 'Name': self.name, 'Description': self.description, 'Price': self.price, 'Roast': self.roast, 'Origin': self.origin, 'Aromas': self.aromas, 'Image': self.image }
        return result
    # Above didn't work properly, was complainign that it was not callable
    # So made the same function with a different name 
    def get_values(self):
        result = { 'ID': self.id, 'Name': self.name, 'Description': self.description, 'Price': self.price, 'Roast': self.roast, 'Origin': self.origin, 'Aromas': self.aromas, 'Image': self.image }
        return result

    def ToJson(self):
        return json.dumps(self.get_values(), sort_keys=True, indent=4)

    @staticmethod
    def ArrayToJson(array):
        products = [product.get_values() for product in array]
        return json.dumps(products, sort_keys=True, indent=4)