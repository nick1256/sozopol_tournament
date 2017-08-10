import mysql.connector as mysqlc
from utilities.create_database import *
from utilities.tables_schema import *
from utilities.inserters import *

def setup(db_name,teams):
		
	# configuration for connector
	config = {
		'user' : 'nick',
		'host' : 'localhost',
	}

	# create connector
	cnx = mysqlc.connect(**config)

	# get cursor 
	cursor = cnx.cursor()

	# create database
	create_database(cursor,db_name)
	cnx.database = db_name

	# navigate to database
	cursor.execute("use {};".format(db_name))
	
	# create tables
	tables = setup_tables(cursor)
	
	# insert teams data
	insert_teams(cursor,teams)	

	# commit the data
	cnx.commit()



