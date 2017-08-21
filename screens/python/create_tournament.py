# kivy imports
from kivy.uix.screenmanager import Screen

# file imports
from utilities.main_setup import setup_database
from utilities.inserters import insert_teams,insert_variables
from utilities.create_connection import create_connection
from screens.python.create_continued import *

# other imports
import os
import mysql.connector as mysqlc
from datetime import datetime
from shutil import rmtree

########## Create Tournament Screen ########## 

class CreateTournamentScreen(Screen):
	
	def __init__(self,name,screen_manager):
		
		super(CreateTournamentScreen,self).__init__()
		self.name = name
		self.window_size = (500,500)
		self.screen_manager = screen_manager

	def get_info(self,nteams1,nteams2,nteams3,nrounds,tname):

		# TODO error check values

		# convert to appropriate types and add to class

		self.nteams_small = int(nteams1)
		self.nteams_medium = int(nteams2)
		self.nteams_big = int(nteams3)
		self.nrounds = int(nrounds)
		self.tname = tname

		# create thre three continue screens, one for each group
		self.screen_manager.add(CreateContinuedScreenSmall("create_continued_small",self.screen_manager,self.nteams_small))
		self.screen_manager.add(CreateContinuedScreenMedium("create_continued_medium",self.screen_manager,self.nteams_medium))
		self.screen_manager.add(CreateContinuedScreenBig("create_continued_big",self.screen_manager,self.nteams_big))

		# go to the one for group 6-7
		self.screen_manager.set("create_continued_small")

	def create_database(self):

		# init database and tell the screen manager to refer to it from now
		setup_database(self.tname)
		self.screen_manager.set_database_name(self.tname)

		# create connection and navigate to database
		cnx = create_connection()
		cnx.database = self.tname

		# get cursor
		cursor = cnx.cursor()

		# create variables dict and insert it into database
		variables = {
			"tournament_name" : self.tname,
			"number_rounds": self.nrounds,
			"number_teams_Small": self.nteams_small,
			"number_teams_Medium": self.nteams_medium,
			"number_teams_Big": self.nteams_big,
			"current_round" : 1
		}

		# insert variables into database
		insert_variables(cursor,variables)
	
		# get team names
		teams1 = self.screen_manager.get_my_screen("create_continued_small").team_names
		teams2 = self.screen_manager.get_my_screen("create_continued_medium").team_names
		teams3 = self.screen_manager.get_my_screen("create_continued_big").team_names

		# insert teams
		insert_teams(cursor,teams1,"Small")
		insert_teams(cursor,teams2,"Medium")
		insert_teams(cursor,teams3,"Big")
		
		# commit and close connection
		cnx.commit()
		cnx.close()
	
		### make dir for this tournament
		
		# directory name
		directory_path = os.getcwd()+"/tournaments/"+self.tname
		
		# delete if already exists
		if os.path.isdir(directory_path): rmtree(directory_path)
		
		# create directory and add init file in it
		os.mkdir(directory_path)
		f = open(directory_path+"/__init__.py",'w')
		f.write("# Do not delete")




