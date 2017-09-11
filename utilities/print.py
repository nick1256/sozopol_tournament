"""create tables for matches """

def print_matches(cursor, category, day):

	"""create tables for matches """

	# get matches
	query = """select team_one, team_two, jury_one, jury_two from Matches_{} where day={}
			;""".format(category, day)

	cursor.execute(query)
	matches = cursor.fetchall()

	# open file
	file_name = open("{}.xlsx".format(category), 'w')
	file_name.write("Team One, Team Two, Jury One, Jury Two, Room \n")

	# write matches
	for match in matches:
		match_name = str(match[0]+', ' + str(match[1]) + ', ' + str(match[2])+', '+str(match[3]))
		file_name.write(match_name+'\n')
