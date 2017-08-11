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
			   visible_name varchar(100) not null unique key
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
