import sqlite3
import json
import Models
import pprint
import sys

print ("running script")

class Database(object):
	# Contructior opens database
	def __init__(self):
		self.select = ""
		self.froms = ""
		self.joins = ""
		self.wheres = ""

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
				print (self.raw_querry(querry))
			except (sqlite3.OperationalError, msg):
				print ("command skipped: ", msg)

	# Gets json and inserts values into databse
	def insert_coffee(self):
		self.open_conn()
		data = open("products.json", 'r')
		jsonData = json.load(data)
		# return jsonData
		for item in jsonData:
			# insert coffees
			querry = 'insert into product (product_id, name, description, price, roast_level, origin) \
					values ({}, "{}", "{}", {}, "{}", "{}")'.format(str(item["ID"]), item["Name"], item["Description"], str(float(item["Price"])), item["Roast"], item["Origin"])
			self.c.execute(querry)

			# insert connection between aromas and coffees
			for aroma in item["Aromas"]:
				if aroma == 'Nutty':
					querry = 'INSERT INTO product_aroma(product_id, aroma_name) VALUES ({}, "{}")'.format(item["ID"], aroma)
				if aroma == 'Fruity':
					querry = 'INSERT INTO product_aroma(product_id, aroma_name) VALUES ({}, "{}")'.format(item["ID"], aroma)
				if aroma == 'Spicy':
					querry = 'INSERT INTO product_aroma(product_id, aroma_name) VALUES ({}, "{}")'.format(item["ID"], aroma)
				if aroma == 'Chocolate':
					querry = 'INSERT INTO product_aroma(product_id, aroma_name) VALUES ({}, "{}")'.format(item["ID"], aroma)
				self.c.execute(querry)
		self.close_conn()
				
	# Drop all tables, Create new table and fill them
	def reset_database(self):
		self.create_table()
		self.insert_coffee()

	# Get one coffee by it's id
	# def get_coffee_by_id(self, id):
	# 	self.open_conn()
	# 	self.c.execute("select *\
	# 					FROM coffee c \
	# 					WHERE c.id = {}\
	# 					".format(id))
	# 	result = self.c.fetchone()
	# 	# Convert list of tuples to list of lists so we can eddit it
	# 	result = list(result)
	# 	aromas = self.get_aromas(id)
	# 	result.append(aromas)
	# 	self.close_conn()
	# 	# id, name, description, price, roast, origin, aromas, image):
	# 	product = Models.Product(result[0], result[1], result[2], result[3], result[4], result[5], result[7], result[6])
	# 	product = product.ToJson()
	# 	return product

	# def get_aromas(self, id):
		# self.c.execute("select a.name \
		# 				FROM coffee_aroma ca \
		# 				INNER JOIN aroma a on ca.aroma_id = a.id \
		# 				WHERE ca.coffee_id = {}".format(id))
		# aromas = self.c.fetchall()
		# # convert list of tuples to list
		# aromas = [elem[0] for elem in aromas]
		# return aromas

	def raw_querry(self, querry):
		self.open_conn()
		self.c.execute(querry)
		result = self.c.fetchall()
		result = [list(elem) for elem in result]
		self.close_conn()
		return result

	# Get information form single table
	# Table; String, name of table
	# Conditios; dictonaty {'Colum name','substring'}
	# def get_from_table(self, table, conditions = {}):
	# 	querry = "select * \
	# 				FROM {} ".format(table)
	# 	if len(conditions) == 1:
	# 		k, v = conditions.items()[0]
	# 		querry += " WHERE {} LIKE '%{}%' ".format(k, v)
	# 	if len(conditions) > 1:
	# 		querry += " WHERE "
	# 		for key, value in conditions.items():
	# 			querry += " {} LIKE '%{}%' AND ".format(key, value)
	# 		querry = querry[:-4]
	# 	return self.raw_querry(querry)

	# rest values for querry
	def reset_querry(self):
		self.select = ""
		self.froms = ""
		self.joins = ""
		self.wheres = ""

	# Build querry form components
	# This funtion makes us of any argumetns passed to where(), join()
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
		if isinstance(value, str):
			value = "'" + value + "'"
		if isinstance(value, int):
			value = str(value)
		if self.wheres == "":
			self.wheres += "WHERE "
		else:
			self.wheres += " AND "
		self.wheres += column +" "+ comparator +" "+ value +" \n"

	# table; string, table name
	# values; dictonary {'columnname':'value'}, columnames and value
	def insert(self, table, values):
		columns = ""
		value = ""
		for key in values:
			if columns == "":
				columns += key
			else:
				columns += ', ' + key
			if value == "":
				if isinstance(values[key], str):
					value += '"' + str(values[key]) + '"'
				else:
					value += str(values[key])
			else:
				if isinstance(values[key], str):
					value += ', "' + str(values[key]) + '"'
				else:
					value += ', ' + str(values[key])
		querry = 'INSERT INTO {}({}) VALUES ({})'.format(table, columns, value)
		return self.raw_querry(querry)

	# table; string, table name
	# values; dictonary (eg {'columnname':'value'}), columnames and value
	# this function also makes use of any arguments passed to where()
	def update(self, table, values):
		updates = ''
		for key in values:
			if updates == '':
				updates += key + ' = '
			else:
				updates += ', ' + key + ' = '
			if isinstance(values[key], str):
				updates += '"' + values[key] +'"'
			else:
				updates += values[key]

		querry = "UPDATE {}\n SET {} \n".format(table, updates)
		if self.wheres != '':
			querry += self.wheres

		result = self.raw_querry(querry)
		self.reset_querry()
		return result

db = Database()
# db.reset_database()

# db.get_colum_names()
# db.where('product_id', 1)
# print db.get_all('product_aroma')

# db.insert('account', {'username' : "Dave", 'password' : "yes", 'name' : 'Arjen', 'surname':'vrijenhoek', 'birth_date':'17-02-1994', 'email':'arjen@arjen.nl', 'banned':0, 'register_date':'31-10-2016', "wishlist_public": 0, 'postal_code':'3205tc', 'house_number':'349'})

# db.where('username', 'Dave')
# db.update("account", {'account_type':'customer'})

# print (db.get_all('account'))


print ("end script")
