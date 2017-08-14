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

	# loop through categories
	for category in ["Small","Medium","Big"]:

		# teams tables
		tables["Teams_{}".format(category)] = (
			"""create table Teams_{}
			   (
		  	       hidden_name  varchar(100) not null unique,
				   visible_name varchar(100) not null unique key,
				   rank_scores  smallint     not null default 0,
				   points       smallint     not null default 0
			   )""".format(category)
		)


		# problems table
		tables['Problems_{}'.format(category)] = (
			"""create table Problems_{}
		       (
				   class    varchar(100) not null,
		 		   day      tinyint      not null,
		           category varchar(100) not null,
		           authors  varchar(100)
			   )
			""".format(category)
		)



		# scores table
		tables['Scores_{}'.format(category)] = (
			"""create table Scores_{}
			   (
		           team  varchar(100) not null unique,
		           day1  tinyint      default null,
		           day2  tinyint      default null,
		           day3  tinyint      default null,
		           day4  tinyint      default null,
		           day5  tinyint      default null,
		           total smallint     default null
		       )
			""".format(category)
		)



	### create all tables ###	
	for table in tables:
		cursor.execute(tables[table])
	
	return tables
