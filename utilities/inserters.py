""" used to insert data in the database """

# insert teams
def insert_teams(cursor, team_names, team_category):

	""" insertion in teams tables """
	for team_name in team_names:

		# create and execute query
		query = """insert into Teams_{} (hidden_name, visible_name)
				 values (\"{}\", \"{}\");""".format(team_category, team_name, team_name)
		cursor.execute(query)

# insert jury member
def insert_jury_member(cursor, values):
	""" insert jury in Jury table"""

	query = """insert into Jury values (\"{}\", {}, {}, {}, {}, {})
		;""".format(values[0], values[1], values[2], values[3], values[4], values[5])
	cursor.execute(query)


def insert_variables(cursor, variables):

	""" insert database variables """

	for variable in variables:

		#create and execute query
		query = "insert into Variables values (\"{}\", \"{}\");".format(variable, variables[variable])
		cursor.execute(query)

def insert_matches(cursor, category, day, matches):
	"""insert matches """

	for match in matches:

		# create and execute query
		query = """insert into Matches_{} values (\"{}\", \"{}\", {}, \"{}\", \"{}\", 0)
			;""".format(category, match[0], match[1], day, match[2], match[3])

		cursor.execute(query)


def insert_problems(cursor, team_category, day, problems):

	""" insert problems """

	for problem in problems:

		query = """insert into Problems_{} values (\"{}\", \"{}\", {})
			;""".format(team_category, problem[0], problem[1], day)

		cursor.execute(query)

# insert people
def insert_people(cursor, category, people):

	""" insert contestors """

	for person in people:

		query = """insert into People_{} (name, team) values (\"{}\", \"{}\")
			;""".format(category, person[0], person[1])

		cursor.execute(query)
