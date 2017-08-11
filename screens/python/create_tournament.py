from kivy.uix.screenmanager import Screen
from screens.python.create_continued import CreateContinuedScreen

from datetime import datetime

########## Create Tournament Screen ########## 

class CreateTournamentScreen(Screen):
	
	def __init__(self,name,screen_manager):
		
		super(CreateTournamentScreen,self).__init__()
		self.name = name
		self.window_size = (300,400)
		self.screen_manager = screen_manager

	def get_info(self,nteams,nrounds,tname):

		# convert to appropriate types and adjust for defaults
		if nteams=="": nteams = 10
		else: nteams = int(nteams)
		
		if nrounds=="" : nrounds = 5
		else: nrounds = int(nrounds)

		if tname=="" :
			tname="Sozopol_" + str(datetime.now().year)		

		# TODO error check values


		# go to continued screen
		self.screen_manager.add_set(CreateContinuedScreen("create_continued",self.screen_manager,nteams,nrounds,tname))
