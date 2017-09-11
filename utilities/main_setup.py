"""setup database and tables in it"""

from utilities.create_database import create_database
from utilities.tables_schema import setup_tables
from utilities.create_connection import create_connection

def setup_database(db_name):

	"""setup database and tables in it"""

	# create conection
	cnx = create_connection()

	# get cursor
	cursor = cnx.cursor()

	# create database and navigate to it
	create_database(cursor, db_name)
	cnx.database = db_name

	# create tables
	setup_tables(cursor)

	# close connection
	cnx.close()
