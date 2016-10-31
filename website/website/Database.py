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
		querrys = open('createdb.sql', 'r').read()
		# print querrys
		querrys = querrys.split(';')
		for querry in querrys:
			try:
				print self.raw_querry(querry)
			except sqlite3.OperationalError, msg:
				print "command skipped: ", msg

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

	def get_aromas(self, id):
		self.c.execute("select a.name \
						FROM coffee_aroma ca \
						INNER JOIN aroma a on ca.aroma_id = a.id \
						WHERE ca.coffee_id = {}".format(id))
		aromas = self.c.fetchall()
		# convert list of tuples to list
		aromas = [elem[0] for elem in aromas]
		return aromas

	def raw_querry(self, querry):
		self.open_conn()
		self.c.execute(querry)
		result = self.c.fetchall()
		# print result[0].keys()
		result = [list(elem) for elem in result]
		self.close_conn()
		return result

	# Get information form single table
	# Table; String, name of table
	# Conditios; dictonaty {'Colum name','substring'}
	def get_from_table(self, table, conditions = {}):
		querry = "select * \
					FROM {} ".format(table)
		if len(conditions) == 1:
			k, v = conditions.items()[0]
			querry += " WHERE {} LIKE '%{}%' ".format(k, v)
		if len(conditions) > 1:
			querry += " WHERE "
			for key, value in conditions.items():
				querry += " {} LIKE '%{}%' AND ".format(key, value)
			querry = querry[:-4]
		return self.raw_querry(querry)

	# rest values for querry
	def reset_querry(self):
		self.select = ""
		self.froms = ""
		self.joins = ""
		self.wheres = ""

	# Build querry form components
	def get_all(self, table, select = "*"):
		self.select = select
		self.froms = table

		querry = "SELECT " + self.select +" \n"
		querry += "FROM " + self.froms + " \n"
		if self.joins != "":
			querry += self.joins

		if self.wheres != "":
			querry += self.wheres

		# print querry

		result = self.raw_querry(querry)
		self.reset_querry()
		return result

	# Add joins to querry
	def join(self, table, condition, type = "INNER"):
		self.joins += type + " JOIN " + table +" ON " + condition +"\n"
		# print self.joins

	# add conditions to querry
	def where(self, column, value, comparator = "="):
		if isinstance(value, basestring):
			value = "'" + value + "'"
		if isinstance(value, int):
			value = str(value)
		if self.wheres == "":
			self.wheres += "WHERE "
		else:
			self.wheres += " AND "
		self.wheres += column +" "+ comparator +" "+ value +" \n"


db = Database()
db.create_table()

# db.get_colum_names()



# db.where("a.name", "Nutty")
# db.where("c.id", 1, ">")
# db.join("coffee_aroma ca", "ca.aroma_id = a.id")
# db.join("coffee c", "ca.coffee_id = c.id")
# print db.get_all("aroma a", "c.id, c.name, a.name")



print "end script"
