# setup tables schema
def setup_tables(cursor):
	
	# all tables and triggers
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
		       name     varchar(100) not null unique,
               Small    bool,
			   Medium   bool,
			   Big      bool,
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
				   points       smallint     not null default 0,
				   points_diff  smallint     not null default 0
			   )""".format(category)
		)
	

		# problems table
		tables['Problems_{}'.format(category)] = (
			"""create table Problems_{}
		       (
				   name     varchar(100) not null,
		           category varchar(100) not null,
				   day      tinyint      not null,
				   unique (name,category,day)
			   )
			""".format(category)
		)


		tables['Matches_{}'.format(category)] = (
			"""create table Matches_{}
			   (
		           team_one      varchar(100) not null,
				   team_two      varchar(100) not null,
				   day           smallint     not null,
				   jury_one      varchar(100) default "",
				   jury_two      varchar(100) default "",
				   protocol_set  bool         default True,
				   unique  (team_one,team_two,day)
		       );
			""".format(category)
		)

		tables['People_{}'.format(category)] = (
			"""create table People_{}
			   (
		           name	        varchar(100) not null,
				   team         varchar(100) not null,
				   alg_scores   smallint     default 0 not null,
				   comb_scores  smallint     default 0 not null,
				   geom_scores  smallint     default 0 not null,
				   num_scores   smallint     default 0 not null,
				   total_scores smallint     default 0 not null,
				   unique (team,name)
		       )
			""".format(category)
		)


	### create all tables ###	
	for table in tables:
		cursor.execute(tables[table])
	
	return tables
