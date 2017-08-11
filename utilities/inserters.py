# used to insert data in the database

# insert teams
def insert_teams(cursor,team_names):
	
	for team_name in team_names:
	
		# query
		query = "insert into teams values (\"{}\",NULL);".format(team_name)
	
		print(query)
		# add to table
		cursor.execute(query)
