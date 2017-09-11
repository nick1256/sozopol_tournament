"""creating a database """
# create database

def create_database(cursor, db_name):
	"""create a database given a cursor and name"""

	# delete database if it exits
	cursor.execute("drop database if exists {};".format(db_name))

	# create new database
	cursor.execute("create database {} default character set 'utf8';".format(db_name))
