import mysql.connector as mysqlc

# create mysql connection to database
def create_connection():

	# configuration for connection
	config = {
		'user' : 'nick',
		'host' : 'localhost',
	}

	# create connection
	cnx = mysqlc.connect(**config)

	# return connection
	return cnx
