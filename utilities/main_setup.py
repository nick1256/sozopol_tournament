from utilities.create_database import *
from utilities.tables_schema import *
from utilities.inserters import *
from utilities.create_connection import *

def setup_database(db_name,*args):
	
	# create conection
	cnx = create_connection()

	# get cursor 
	cursor = cnx.cursor()

	# create database and navigate to it
	create_database(cursor,db_name)
	cnx.database = db_name

	
	# create tables
	tables = setup_tables(cursor)

	# close connection
	cnx.close()
