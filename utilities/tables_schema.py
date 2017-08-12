# setup tables schema
def setup_tables(cursor):
	
	# all tables
	tables = {}

	### configure schemas ###

	# variables table
	tables["Variables"] = (
		"""create table Variables
		   (
               name  varchar(100) not null unique,
			   value varchar(100) not null
		   );"""
	)
	

	# teams tables
	tables["Teams_Small"] = (
		"""create table Teams_Medium
		   (
	  	       hidden_name  varchar(100) not null unique,
			   visible_name varchar(100) not null unique key
		   );"""
	)

	tables["Teams_Medium"] = (
		"""create table Teams_Big
		   (
	  	       hidden_name  varchar(100) not null unique,
			   visible_name varchar(100) not null unique key
		   );"""
	)

	tables["Teams_Big"] = (
		"""create table Teams_Small 
		   (
	  	       hidden_name  varchar(100) not null unique,
			   visible_name varchar(100) not null unique key
		   );"""
	)


	
	# jury table
	tables['Jury'] = (
		"""create table Jury
		   (
		       f_name varchar(100) not null,
               l_name varchar(100) not null,
               pref   varchar(100) not null default '-'
		   )
        """
	)



	# problems table
	tables['Problems'] = (
		"""create table Problems
           (
		       class    varchar(100) not null,
	 		   day      tinyint      not null,
               category varchar(100) not null,
               authors  varchar(100)
		   )
		"""
	)



    # scores table
	tables['Scores'] = (
		"""create table Scores
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
	
	return tables
