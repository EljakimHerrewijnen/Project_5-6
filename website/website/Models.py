import json
from website import Database
from datetime import date

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
    def _fromSql(sqlFile):
        db = Database.Database()
        db.where("product_id", sqlFile["product_id"]);
        aromas = []
        for item in db.get_all("product_aroma", "aroma_name"):
            aromas.append(item['aroma_name'])

        return Product(
            sqlFile["product_id"],
            sqlFile["name"],
            sqlFile["description"],
            float(sqlFile["price"]),
            sqlFile["roast_level"],
            sqlFile["origin"],
            aromas,
            "images/" + str(sqlFile["product_id"]) + ".jpg"
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
        #data = open("website/products.json", 'r')
        db = Database.Database()

        data = db.get_all("product")

        products = []
        for item in data:
            products.append(Product._fromSql(item))
        return products
        
    @staticmethod
    def find(search_id = None):
        products = Product.get_all()
        if (search_id):
            products = list(filter(lambda product: str(product.id) == search_id, products))
        return products[0]

    def __dict__(self):
        result = { 'id': self.id, 'name': self.name, 'description': self.description, 'price': self.price, 'roast': self.roast, 'origin': self.origin, 'aromas': self.aromas, 'image': self.image }
        return result

    # Above didn't work properly, was complainign that it was not callable
    # So made the same function with a different name 
    def get_values(self):
        result = { 'id': self.id, 'name': self.name, 'description': self.description, 'price': self.price, 'roast': self.roast, 'origin': self.origin, 'aromas': self.aromas, 'image': self.image }
        return result

    def ToJson(self):
        return json.dumps(self.get_values(), sort_keys=True, indent=4)

    @staticmethod
    def ArrayToJson(array):
        products = [product.get_values() for product in array]
        return json.dumps(products, sort_keys=True, indent=4)

