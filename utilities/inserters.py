# used to insert data in the database

# insert teams
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
