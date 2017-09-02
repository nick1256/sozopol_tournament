# mysql imports
import mysql.connector as mysqlc
from mysql.connector import errorcode

# file imports
from utilities.create_connection import create_connection
from utilities.inserters import insert_matches

def generate_round(database_name,category,day):
	
	# connect to database
	cnx = create_connection()
	cnx.database = database_name
	cursor = cnx.cursor()

	# get teams sorted according to scores 
	query = "select visible_name,rank_scores,points from Teams_{} order by rank_scores,points;".format(category)
	cursor.execute(query)
	teams = cursor.fetchall()	

	# get jury members for category
	query = "select name from Jury where {}=1 and active=1;".format(category)
	cursor.execute(query)
	jury = cursor.fetchall()

	# split into matches
	matches = split_teams(teams,jury)

	# clear matches table if previous assignment exists and put new one
	cursor.execute("delete from Matches_{} where day={}".format(category,day))
	insert_matches(cursor,category,day,matches)
	
	print(matches)

	# commit data
	cnx.commit()



def split_teams(teams,jury):
	
	nteams = len(teams)
	njury = len(jury)
	nmatches = nteams//2	

	if njury<nmatches: 
		raise ValueError("Not Enough Jury Members")

	matches = [[teams[2*i][0],teams[2*i+1][0],jury[i][0]] for i in range(nmatches)]
	
	# add extra jury members
	
	counter = 0
	while counter<nmatches:
		if counter+nmatches<njury:
			matches[counter].append(jury[counter+nmatches][0])
		else:
			matches[counter].append("Null")
		counter+=1

	if nteams%2==1:
		matches.append([teams[-1][0],teams[-1][0],"Null","Null"])
	
	return matches
