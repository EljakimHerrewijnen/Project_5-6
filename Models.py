import json

class Product:
    def __init__(self, name = "", description = "", price = ""):
        self.name = name
        self.description = description
        self.price = price

    @staticmethod
    def get_all():
        data = open("products.json", 'r')
        jsonData = json.load(data)
        
        products = []
        for item in jsonData:
            products.append(Product(item['Name'], item['Description'], float(item['Price'])))

        return products

    @staticmethod
    def get_by_name(name, products = None):
        if (products == None):
            products = Product.get_all()

        products = filter(lambda x: name in x.name, products)
        return products

    @staticmethod
    def get_by_price(min, max, products = None):
        if (products == None):
            products = Product.get_all()
        
        products = filter(lambda x: min <= x.price <= max, products)
        return products

    def __dict__(self):
        result = { 'Name': self.name, 'Description': self.description, 'Price': self.price }
        return result

    def ToJson(self):
        return json.dumps(self.__dict__(), sort_keys=True, indent=4)

    @staticmethod
    def ArrayToJson(array):
        products = [product.__dict__() for product in array]
        return json.dumps(products, sort_keys=True, indent=4)