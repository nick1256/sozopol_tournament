import mysql.connector as mysqlc

from mysql.connector import errorcode
from utilities.parsers import *
from utilities.main_setup import setup

# testing
if __name__=='__main__':
	teams = parse_teams('teams_example.csv')
	jury = parse_jury('jury_example.csv')
	setup('sozopol_2017',teams,jury)
