# used to insert data in the database
import mysql.connector as mysqlc
# insert teams
def insert_teams(cursor,team_names,team_category):
	
	for team_name in team_names:
		
		# create and execute query
		query = "insert into Teams_{} values (\"{}\",\"{}\");".format(team_category,team_name,team_name)
		cursor.execute(query)


# insert database variables
def insert_variables(cursor,variables):
	
	for variable in variables:
		
		#create and execute query
		query = "insert into Variables values (\"{}\",\"{}\")".format(variable,variables[variable])
		cursor.execute(query)

