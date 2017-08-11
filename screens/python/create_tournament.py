from kivy.uix.screenmanager import Screen
from screens.python.create_continued import CreateContinuedScreen

from datetime import datetime

########## Create Tournament Screen ########## 

class CreateTournamentScreen(Screen):
	
	def __init__(self,name,screen_manager):
		
		super(CreateTournamentScreen,self).__init__()
		self.name = name
		self.window_size = (500,500)
		self.screen_manager = screen_manager

	def get_info(self,nteams1,nteams2,nteams3,nrounds,tname):

		# convert to appropriate types and adjust for defaults
		if nteams1=="": nteams1 = 18
		else: nteams1 = int(nteams1)

		if nteams2=="": nteams2 = 14
		else: nteams2 = int(nteams2)

		if nteams3=="": nteams3 = 8
		else: nteams3 = int(nteams3)
		
		if nrounds=="" : nrounds = 5
		else: nrounds = int(nrounds)

		if tname=="" :
			tname="Sozopol_" + str(datetime.now().year)		

		# TODO error check values


		# create three continued screens
		self.screen_manager.add(CreateContinuedScreen("create_continued_6-7",self.screen_manager,nteams1,nrounds,tname))
		self.screen_manager.add(CreateContinuedScreen("create_continued_8-9",self.screen_manager,nteams2,nrounds,tname))
		self.screen_manager.add(CreateContinuedScreen("create_continued_10-12",self.screen_manager,nteams3,nrounds,tname))

		# go to the one for 6-7 group
		self.screen_manager.set("create_continued_6-7")
