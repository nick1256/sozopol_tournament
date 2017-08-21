# mysql imports
import mysql.connector as mysqlc
from mysql.connector import errorcode

# file imports
from utilities.create_connection import create_connection
from utilities.inserters import insert_matches

def generate_round(database_name,category):
	
	# connect to database
	cnx = create_connection()
	cnx.database = database_name
	cursor = cnx.cursor()

	# get teams sorted according to scores 
	query = "select visible_name,rank_scores,points from Teams_{} order by rank_scores,points;".format(category)
	cursor.execute(query)
	teams = cursor.fetchall()	

	# split into matches
	matches = split_teams(teams)

	# clear matches table if not empty and put matches into matches table
	cursor.execute("truncate Matches_{}".format(category))
	insert_matches(cursor,category,matches)
	
	# commit data
	cnx.commit()



def split_teams(teams):
	
	nteams = len(teams)

	matches = [(teams[2*i][0],teams[2*i+1][0]) for i in range(nteams//2)]
	if nteams%2==1:
		matches.append((teams[-1][0],teams[-1][0]))
	
	return matches
