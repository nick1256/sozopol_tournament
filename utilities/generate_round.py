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
	
	# clear matches table if previous assignment 
	cursor.execute("delete from Matches_{} where day={}".format(category,day))
	cnx.commit()
	
	# split into matches
	matches = split_teams(cursor,category)

	# insert matches
	insert_matches(cursor,category,day,matches)

	# commit data
	cnx.commit()


# backtracking search
def backtrack_search(team_names,domains):
	return backtrack(True,[],team_names,domains)

def backtrack(at_start,assignment,team_names,domains):

	# assignment is complete
	if len(team_names)==0:
		return assignment
	
	first_team = team_names[0]
	for second_team in team_names:

		if second_team not in domains[first_team]: continue

		new_team_names = [i for i in team_names if i!=first_team and i!=second_team]
		new_assignment=[i for i in assignment]
		new_assignment.append([first_team,second_team])

		result = backtrack(False,new_assignment,new_team_names,domains)

		if result!=None:
			return result
	
	return None



def split_teams(cursor,category):

	# get teams sorted according to scores 
	query = "select visible_name,rank_scores,points_diff,points from Teams_{} order by rank_scores desc, points_diff desc".format(category)
	cursor.execute(query)
	
	# full info
	teams_info = cursor.fetchall()

	# names only	
	team_names = [teams[0] for teams in teams_info]	
	nteams = len(team_names)

	
	forbidden_matches = dict()
	# create intitial list containing
	for team_name in team_names:
		forbidden_matches[team_name]=[team_name]	



	# get jury members for category split into alone and extra
	query = "select name,alone from Jury where {}=1 and active=1 and alone=1;".format(category)
	cursor.execute(query)
	alone_jury = [result[0] for result in cursor.fetchall()]

	query = "select name,alone from Jury where {}=1 and active=1 and alone=0;".format(category)
	cursor.execute(query)
	extra_jury = [result[0] for result in cursor.fetchall()]
	
	# number of matches
	nmatches = nteams//2
	
	### find a team to get free win if uneven number of teams

	# find teams that have had a free win
	query = "select team_one from Matches_{} where team_one=team_two;".format(category)	
	cursor.execute(query)
	free_win_teams = set([result[0] for result in cursor.fetchall()])

	# choose one and remove it from teams
	if nteams%2==1:
		# find teams with minimal score that have not yet had a free win 
		m = min([team[1] for team in teams_info if team not in free_win_teams])
		
		# primitive randomizing
		lowest = set([team for team in teams_info if team[1]==m])
		lowest = [i for i in lowest]
		
		# pick a free winner
		free_winner = lowest[0][0]
		team_names.remove(free_winner)

	# create a set of all matches that have happened
	query = "select team_one,team_two from Matches_{} where team_one!=team_two;".format(category)
	cursor.execute(query)
		
	

	for match in cursor.fetchall():
		
		team_one = match[0]
		team_two = match[1]

		forbidden_matches[team_one].append(team_two)
		forbidden_matches[team_two].append(team_one)

	domains = {}

	for team_name in team_names:
		domains[team_name] = [other_team_name for other_team_name in team_names if other_team_name not in forbidden_matches[team_name]]

	# try to find solution
	matches = backtrack_search(team_names,domains)

	# safe guard
	if matches=="Failure":
		matches = [[team_names[2*i],team_names[2*i+1]] for i in range(len(team_names)//2)] 


	# primitive randomizing
	alone_jury = set(alone_jury)
	alone_jury = [i for i in alone_jury]
	extra_jury = set(extra_jury)
	extra_jury = [i for i in extra_jury]

	counter = 0

	if "Николай Стоянов" in alone_jury:
		matches[counter].append('Николай Стоянов')
		counter+=1
		alone_jury.remove("Николай Стоянов")

	while counter!=nmatches and len(alone_jury)!=0:
		name = alone_jury.pop(0)
		matches[counter].append(name)
		counter+=1

	if counter==nmatches:
		counter-=1
		while counter!=-1 and len(alone_jury)!=0:
			name = alone_jury.pop(0)
			matches[counter].append(name)
			counter-=1
	
		while counter!=-1 and len(extra_jury)!=0:
			name = extra_jury.pop(0)
			matches[counter].append(name)
			counter-=1
	
	else:
		while counter<nmatches and len(extra_jury)!=0:
			name = extra_jury.pop(0)
			matches[counter].append(name)
			counter+=1

		counter-=1
		while counter!=-1 and len(extra_jury)!=0:
			name = extra_jury.pop(0)
			matches[counter].append(name)
			counter-=1

	for match in matches:
		t = 4-len(match)
		for i in range(t):
			match.append("")

	# if there is a free winner, add him to the table of matches with no jury
	if nteams%2==1:
		matches.append([free_winner,free_winner,"Null","Null"])

	return matches
