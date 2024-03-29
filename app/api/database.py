import sqlite3
import json
import sys
import os


class Database(object):
	# Contructior opens database
	def __init__(self, databasePath = "app/data.db"):
		self.databasePath = databasePath
		self.select = ""
		self.froms = ""
		self.joins = ""
		self.wheres = ""
		self.groupBy = ""
		self.orderBy = ""

	def open_conn(self):
		# api route

		dirpath = os.path.dirname(os.path.realpath(__file__)) + "/../../"
		pathlength = len(os.getcwd())

		if(pathlength != 1): 
			skipchars = pathlength + 1
		else: 
			skipchars = 1
		
		self.databaseRelativeLocation = dirpath[skipchars:] + self.databasePath

		self.conn = sqlite3.connect(self.databaseRelativeLocation)

		# this file test use route
		self.c = self.conn.cursor()
		self.conn.row_factory = sqlite3.Row

	def close_conn(self):
		self.conn.commit()
		self.conn.close()

	# Create releavant tables
	# Only use if you know what you are doing!!!
	def create_table(self):
		tables = ["address", "user_address", "product", "product_aroma", "wishes", "account", "favorites", "orders", "order_details"]
		for table in tables:
			query = "DROP TABLE IF EXISTS " + table
			self.raw_querry(query)
		# print("tables deleted")
		queryFile = open('app/api/createdb.sql', 'r')
		querrys = queryFile.read()
		queryFile.close()
		querrys = querrys.split(';')
		for querry in querrys:
			try:
				self.raw_querry(querry)
			except (sqlite3.OperationalError, msg):
				print ("command skipped: ", msg)

	# Gets json and inserts values into databse
	def insert_coffee(self):
		self.open_conn()
		data = open("app/products.json", 'r')
		jsonData = json.load(data)
		data.close()
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

	def raw_get_one_querry(self, querry):
		try:
			self.open_conn()
			self.c.execute(querry)
			result = self.c.fetchone()
			names = [description[0] for description in self.c.description]
			final = {}
			if result != None:
				for i in range(0, len(result)):
					final[names[i]] = result[i]
			self.close_conn()
		except:
			final = sys.exc_info()
		return final

	# executes given query
	# returns number of rows affected by query or last rowid
	def raw_querry(self, querry, rowcount = True):
		try:
			self.open_conn()
			self.c.execute(querry)
			if rowcount:
				result = self.c.rowcount
			else:
				result = self.c.lastrowid
			self.close_conn()
		except:
			result = sys.exc_info()
			print(result)
			print("raw query error")
			print(querry)
		return result

	# rest values for querry
	def reset_querry(self):
		self.select = ""
		self.froms = ""
		self.joins = ""
		self.wheres = ""
		self.groupBy = ""
		self.orderBy = ""

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
		if self.groupBy != "":
			querry += self.groupBy
		if self.orderBy != "":
			querry += self.orderBy

		result = self.raw_get_querry(querry)
		self.reset_querry()
		return result

	# Build querry form components
	# This funtion makes us of any argumetns passed to where(), join()
	def get_one(self, table, select = "*"):
		self.select = select
		self.froms = table

		querry = "SELECT " + self.select +" \n"
		querry += "FROM " + self.froms + " \n"
		if self.joins != "":
			querry += self.joins
		if self.wheres != "":
			querry += self.wheres
		if self.groupBy != "":
			querry += self.groupBy
		if self.orderBy != "":
			querry += self.orderBy

		result = self.raw_get_one_querry(querry)
		self.reset_querry()
		return result

	# Add joins to querry
	def join(self, table, condition, type = "INNER"):
		self.joins += type + " JOIN " + table +" ON " + condition +"\n"

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
	# return; last rowid
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
		return self.raw_querry(querry, False)

	# table; string, table name
	# values; dictonary (eg {'columnname':'value'}), columnames and value
	# this function also makes use of any arguments passed to where()
	# return;
	def update(self, table, values):
		updates = ''
		for key in values:
			if updates == '':
				updates += key + ' = '
			else:
				updates += ', ' + key + ' = '
			if isinstance(values[key], str):
				updates += '"' + values[key] +'"'
			elif isinstance(values[key], int):
				updates += "'" + str(values[key]) + "'"
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
	# return; number of rows affected
	def delete(self, table):
		querry = 'DELETE FROM {} \n'.format(table)
		if self.wheres != '':
			querry += self.wheres
		self.reset_querry()
		return self.raw_querry(querry)

	# column: string, column you want to group by
	# This function adds a group by argument to your query
	def group_by(self, column):
		if self.groupBy == "":
			self.groupBy += "GROUP BY " + column
		else:
			self.groupBy += " , "+ column

	def order_by(self, column):
		if self.orderBy == "":
			self.orderBy += "ORDER BY " + column
		else:
			self.orderBy += " , "+ column

	# Converts given to json.
	def to_jsonarray(self, array):
		return json.dumps(array, ensure_ascii=False, sort_keys=True)
