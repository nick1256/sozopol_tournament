import mysql.connector as mysqlc
from mysql.connector import errorcode



########### Utilities ##########

# setup tables schema
def setup_tables(cursor):
	
	# all tables
	tables = {}
	
	### configure schemas ###

	# teams table
	tables['teams'] = (
    	"""create table teams 
		   (
      	       hidden_name  varchar(100) unique,
			   visible_name varchar(100) not null unique key,
			   category     varchar(100) not null
		   );"""
	)
	
	# trigger to set visible_name to hidden_name if visible_name = NULL
	trigger = """ create trigger foo before insert on teams for each row
    			      if new.visible_name is null then
        			      set new.visible_name := new.hidden_name;
    				  end if;;
			  """
	
	# jury table
	tables['jury'] = (
		"""create table jury
		   (
		       f_name varchar(100) not null,
               l_name varchar(100) not null,
               pref   varchar(100) not null default '-'
		   )
        """
	)

	# problems table
	tables['problems'] = (
		"""create table problems
           (
		       class    varchar(100) not null,
	 		   day      tinyint      not null,
               category varchar(100) not null,
               authors  varchar(100)
		   )
		"""
	)

    # scores table
	tables['scores'] = (
		"""create table scores
		   (
               team  varchar(100) not null unique,
               day1  tinyint      not null,
               day2  tinyint      not null,
               day3  tinyint      not null,
               day4  tinyint      not null,
               day5  tinyint      not null,
               total smallint     not null
           )
		"""
	)


	### create all tables ###	
	for table in tables:
		cursor.execute(tables[table])
	cursor.execute(trigger)	

	return tables

# create database  
def create_database(cursor,db_name):
	
	# delete database if it exits
	cursor.execute(
		"drop database if exists {};".format(db_name))
	
	# create new database
	cursor.execute(
		"create database {} default character set 'utf8'".format(db_name))

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


def insert_teams(cursor,teams):
	
	for team in teams:
	
		# get information
		hn = team;
		vn = teams[team]['visible_name']
		ct = teams[team]['category']
		
		# query
		query = "insert into teams values (\"{}\",\"{}\",\"{}\");".format(hn,vn,ct)
	
		# add to table
		cursor.execute(query)


def insert_jury(cursor,juries):
		
	for jury in juries:
		
		# get information
		fname = 


		# query

		# add to table


##### main callable function #####

# parses teams file
def parse_teams(filename):

	# open file for reading	
	f = open(filename,'r')

	# get number of teams	
	num_of_teams = int(f.readline().split(':')[1])
	
	# dict of teams (name)-> rest
	teams = {}
	
	# get teams TODO error_check
	for i in range(num_of_teams):
		contents = f.readline().split(',')
		
		# get hidden name
		hidden_name = contents[0]

		# get additional information
		# account for '\n' in category
		information = {
			'visible_name' : contents[1],
			'category': contents[2][:-1],
		}

		# add team to all teams		
		teams[hidden_name] = information
	
	return teams

# testing
if __name__=='__main__':
	teams = parse_teams('teams_example.csv')
	setup('sozopol_2017',teams)
