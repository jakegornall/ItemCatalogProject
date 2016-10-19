import sqlite3

# name your database
database = 'ItemCatalog.db'

with open('databaseSetupScript.sql', 'r') as databaseSetupScript:
	databaseSetupScript = databaseSetupScript.read().replace('\n', '').replace('\t', '')

if not databaseSetupScript:
	print "database setup script unavailable."

else:
	DBactionList = databaseSetupScript.split(';')
	print DBactionList

	for i in DBactionList:
		conn = sqlite3.connect(database)
		if not conn:
			print "Could not connect to database."
			break
		c = conn.cursor()
		c.execute(i)
		conn.commit()
		conn.close()
	print "Database Successfully Created!"
