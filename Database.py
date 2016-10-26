import sqlite3
import json
import pprint


print "running script"

class Database(object):
	# Contructior opens database
	def __init__(self):
		self.conn = sqlite3.connect("db.sqlite")
		self.c = self.conn.cursor()

	# Create releavant tables 
	# Only use if you know what you are doing!!!
	def create_table(self):
		self.c.execute("drop table coffee")
		self.c.execute("drop table aroma")
		self.c.execute("drop table coffee_aroma")
		self.c.execute('CREATE TABLE coffee (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, description TEXT, price REAL, roast TEXT, origin TEXT, picture TEXT)')
		self.c.execute('CREATE TABLE aroma (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT)')
		self.c.execute('CREATE TABLE coffee_aroma (id INTEGER PRIMARY KEY AUTOINCREMENT, coffee_id INT, aroma_id INT)')

	# Instert some data into a table
	def insert_aroma(self):
		self.c.execute('insert into aroma (name) values ("Nutty")')
		self.c.execute('insert into aroma (name) values ("Fruity")')
		self.c.execute('insert into aroma (name) values ("Spicy")')
		self.c.execute('insert into aroma (name) values ("Chocolate")')
		test = "pie"
		self.c.execute('insert into aroma (name) values ("'+ test +'")')

	# Gets json and inserts values into databse
	def insert_coffee(self):
		# products = Models.Product.get_all()
		# products = Models.Product.ArrayToJson(products)
		# return products
		data = open("products.json", 'r')
		jsonData = json.load(data)
		# return jsonData
		for item in jsonData:
			# insert coffees
			querry = 'insert into coffee (id, name, description, price, roast, origin, picture) values ({}, "{}", "{}", {}, "{}", "{}", "{}")'.format(str(item["ID"]), item["Name"], item["Description"], str(float(item["Price"])), item["Roast"], item["Origin"], item["Image"])
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

			# self.c.execute('insert into coffee (id, name, description, price, roast, origin, picture) values ({}, "{}", "{}", {}, "{}", "{}", "{}")'.format(item["ID"], item["Name"], item["Description"], float(item["Price"]), item["Roast"], item["Origin"], item["Image"]))
			# self.c.execute('insert into coffee (id, name, description, price, roast, origin, picture) values ('+ item["ID"] +',"'+ item["Name"] +'","'+ item["Description"] +'",'+ float(item["Price"]) +',"'+ item["Roast"] +'"'+ item["Origin"] +'","'+ item["Image"] +'")')
			# item["ID"], item["Name"], item["Description"], float(item["Price"]), item["Roast"], item["Origin"], item["Image"]
			# for aroma in item["Aromas"]
				
		# return item
		

	# Drop all tables, Create new table and fill them
	def reset_database(self):
		self.create_table()
		self.insert_aroma()
		self.insert_coffee()

	# Get all from table
	def get_all(self):
		self.c.execute("select * \
						FROM coffee c \
						INNER JOIN coffee_aroma ca on c.id = ca.coffee_id\
						INNER JOIN aroma a on ca.aroma_id = a.id\
						")
		return self.c.fetchall()


		
db = Database()
db.reset_database()
# print db.insert_coffee()

result = db.get_all()
print(result)

db.conn.close()


print "end script"
