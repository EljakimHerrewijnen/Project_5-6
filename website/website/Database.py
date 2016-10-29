import sqlite3
import json
import Models
import pprint

print "running script"

class Database(object):
	# Contructior opens database
	def __init__(self):
		# test
		a=1

	def open_conn(self):
		self.conn = sqlite3.connect("data.db")
		self.c = self.conn.cursor()

	def close_conn(self):
		self.conn.commit()
		self.conn.close()

	# Create releavant tables 
	# Only use if you know what you are doing!!!
	def create_table(self):
		self.open_conn()
		self.c.execute("drop table coffee")
		self.c.execute("drop table aroma")
		self.c.execute("drop table coffee_aroma")
		self.c.execute('CREATE TABLE coffee (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, description TEXT, price REAL, roast TEXT, origin TEXT, picture TEXT)')
		self.c.execute('CREATE TABLE aroma (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT)')
		self.c.execute('CREATE TABLE coffee_aroma (id INTEGER PRIMARY KEY AUTOINCREMENT, coffee_id INT, aroma_id INT)')
		self.close_conn()


	# Instert some data into a table
	def insert_aroma(self):
		self.open_conn()
		self.c.execute('insert into aroma (name) values ("Nutty")')
		self.c.execute('insert into aroma (name) values ("Fruity")')
		self.c.execute('insert into aroma (name) values ("Spicy")')
		self.c.execute('insert into aroma (name) values ("Chocolate")')
		self.close_conn()
		

	# Gets json and inserts values into databse
	def insert_coffee(self):
		self.open_conn()
		data = open("products.json", 'r')
		jsonData = json.load(data)
		# return jsonData
		for item in jsonData:
			# insert coffees
			querry = 'insert into coffee (id, name, description, price, roast, origin, picture) \
					values ({}, "{}", "{}", {}, "{}", "{}", "{}")'.format(str(item["ID"]), item["Name"], item["Description"], str(float(item["Price"])), item["Roast"], item["Origin"], item["Image"])
			self.c.execute(querry)

			# insert connection between aromas and coffees
			for aroma in item["Aromas"]:
				if aroma == 'Nutty':
					querry = 'INSERT INTO coffee_aroma(coffee_id, aroma_id) VALUES ({}, {})'.format(item["ID"], 1)
				if aroma == 'Fruity':
					querry = 'INSERT INTO coffee_aroma(coffee_id, aroma_id) VALUES ({}, {})'.format(item["ID"], 2)
				if aroma == 'Spicy':
					querry = 'INSERT INTO coffee_aroma(coffee_id, aroma_id) VALUES ({}, {})'.format(item["ID"], 3)
				if aroma == 'Chocolate':
					querry = 'INSERT INTO coffee_aroma(coffee_id, aroma_id) VALUES ({}, {})'.format(item["ID"], 4)
				self.c.execute(querry)
		self.close_conn()
				
	# Drop all tables, Create new table and fill them
	def reset_database(self):
		self.create_table()
		self.insert_aroma()
		self.insert_coffee()

	# Get one coffee by it's id
	def get_coffee_by_id(self, id):
		self.open_conn()
		self.c.execute("select *\
						FROM coffee c \
						WHERE c.id = {}\
						".format(id))
		result = self.c.fetchone()
		# Convert list of tuples to list of lists so we can eddit it
		result = list(result)
		aromas = self.get_aromas(id)
		result.append(aromas)
		self.close_conn()
		# id, name, description, price, roast, origin, aromas, image):
		product = Models.Product(result[0], result[1], result[2], result[3], result[4], result[5], result[7], result[6])
		product = product.ToJson()
		return product

	# Get all from table
	def get_all(self, filter = None):
		querry = "select *\
				FROM coffee c"

		self.open_conn()
		self.c.execute(querry)
		result = self.c.fetchall()
		# Convert list of tuples to list of lists so we can eddit it
		result = [list(elem) for elem in result]
		products = []
		for coffee in result:
			aromas = self.get_aromas(coffee[0])
			coffee.append(aromas)
			product = Models.Product(coffee[0], coffee[1], coffee[2], coffee[3], coffee[4], coffee[5], coffee[7], coffee[6])
			products.append(product)

		self.close_conn()
		products = Models.Product.ArrayToJson(products)
		return products

	def get_aromas(self, id):
		self.c.execute("select a.name \
						FROM coffee_aroma ca \
						INNER JOIN aroma a on ca.aroma_id = a.id \
						WHERE ca.coffee_id = {}".format(id))
		aromas = self.c.fetchall()
		# convert list of tuples to list
		aromas = [elem[0] for elem in aromas]
		return aromas


db = Database()
# db.reset_database()

# result = db.get_all()
result = db.get_coffee_by_id(5)
# result = Models.Product.ArrayToJson(result)
print(result)



print "end script"
