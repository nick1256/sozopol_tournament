# used to insert data in the database

# insert teams
def insert_teams(cursor,team_names1,team_names2,team_names3):
	
	for team_name in team_names1:
		query = "insert into Teams_{} values (\"{}\",NULL);".format(team_name)
		# add to table
		cursor.execute(query)

	for team_name in team_names2:
		query = "insert into Teams_{} values (\"{}\",NULL);".format(team_name)
		# add to table
		cursor.execute(query)

	for team_name in team_names3:
		query = "insert into Teams_{} values (\"{}\",NULL);".format(team_name)
		# add to table
		cursor.execute(query)
