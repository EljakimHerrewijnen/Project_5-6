import sqlite3

print "running script"



class Database(object):

	def __init__(self):
		self.conn = sqlite3.connect("db.sqlite")
		self.c = self.conn.cursor()

	def create_table(self):
		print "creating"

		self.c.execute('CREATE TABLE cofee (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, description TEXT, price REAL, origin TEXT, picture BLOB)')
		self.c.execute('CREATE TABLE aroma (id INT primary key NOT NULL, name TEXT)')
		self.c.execute("drop table cofee")

	def insert(self):
		self.c.execute('insert into cofee (name) values ("pie")')
		self.c.execute('insert into cofee (name) values ("thee")')


	def get_all(self):
		self.c.execute("select * from cofee")
		return self.c.fetchall()



db = Database()
# db.create_table()
# result = db.get_all()
# print(result)

db.conn.close()


print "end script"
