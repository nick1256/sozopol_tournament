# create database  
def create_database(cursor,db_name):
	
	# delete database if it exits
	cursor.execute(
		"drop database if exists {};".format(db_name))
	
	# create new database
	cursor.execute(
		"create database {} default character set 'utf8';".format(db_name))

