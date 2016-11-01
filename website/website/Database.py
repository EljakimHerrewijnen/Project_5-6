import sqlite3
import json
import Models
import pprint
import sys

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
		self.conn.row_factory = sqlite3.Row

	def close_conn(self):
		self.conn.commit()
		self.conn.close()

	# Create releavant tables 
	# Only use if you know what you are doing!!!
	def create_table(self):
		querrys = open('createdb.sql', 'r').read()
		querrys = querrys.split(';')
		for querry in querrys:
			try:
				print (self.raw_get_querry(querry))
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

	def raw_get_querry(self, querry):
		try:
			self.open_conn()
			self.c.execute(querry)
			result = self.c.fetchall()
			names = [description[0] for description in self.c.description]
			final = []
			for elem in result:
				tempdict = {}
				for value in range(0, len(elem)):
					tempdict[names[value]] = elem[value]
				final.append(tempdict)
			self.close_conn()
		except:
			final = sys.exc_info()
		return final

	def raw_querry(self, querry):
		try:
			self.open_conn()
			self.c.execute(querry)
			result = self.c.fetchall()
			result = [list(elem) for elem in result]
			names = [description[0] for description in self.c.description]
			self.close_conn()
			final = []
			final.append(names)
			final.append(result)
			final = self.c.description
			self.close_conn()
		except:
			final = sys.exc_info()
		return final

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

		result = self.raw_get_querry(querry)
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
			columns += key + ', '
			if isinstance(values[key], str):
				value += '"' + str(values[key]) + '", '
			else:
				updates += values[key]

		querry = "UPDATE {}\n SET {} \n".format(table, updates)
		if self.wheres != '':
			querry += self.wheres

		result = self.raw_querry(querry)
		self.reset_querry()
		return result

	# table: string, table name
	# this function also uses the arguments passed to where()
	def delete(self, table):
		querry = 'DELETE FROM {} \n'.format(table)
		if self.wheres != '':
			querry += self.wheres
		self.reset_querry()
		return self.raw_querry(querry)

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

	# table: string, table name
	# this function also uses the arguments passed to where()
	def delete(self, table):
		querry = 'DELETE FROM {} \n'.format(table)
		if self.wheres != '':
			querry += self.wheres
		self.reset_querry()
		return self.raw_querry(querry)

db = Database()
EljakimQuery = db.get_all('product')

with open('website/Eljakim.json', 'w') as outfile:
	json.dump(EljakimQuery, outfile, ensure_ascii=False, indent=2, sort_keys=True)
print ("end script")
