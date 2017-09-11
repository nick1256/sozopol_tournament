# file imports
from utilities.create_connection import create_connection

# mysql imports
import mysql.connector as mysqlc
from mysql.connector import errorcode

def print_matches(cursor,category,day):
	
	# get matches
	query = "select team_one,team_two,jury_one,jury_two from Matches_{} where day={};".format(category,day)
	cursor.execute(query)
	matches = cursor.fetchall()

	# open file
	f = open("{}.xlsx".format(category),'w')
	f.write("Team One,Team Two,Jury One,Jury Two,Room \n")

	# write matches
	for match in matches:
		match_name = str(match[0]+',' + str(match[1]) + ',' + str(match[2])+','+str(match[3]))
		f.write(match_name+'\n')


