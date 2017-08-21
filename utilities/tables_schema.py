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
		       name     varchar(100) not null,
               small    bool,
			   medium   bool,
			   big      bool,
			   alone    bool,
			   active   bool
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

		tables['Matches_{}'.format(category)] = (
			"""create table Matches_{}
			   (
		           team_one  varchar(100) not null,
				   team_two  varchar(100) not null,
				   jury_one  varchar(100) default null,
				   jury_two  varchar(100) default null
		       )
			""".format(category)
		)

	### create all tables ###	
	for table in tables:
		cursor.execute(tables[table])
	
	return tables
