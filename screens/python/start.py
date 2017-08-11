from kivy.uix.screenmanager import Screen
from screens.python.create_tournament import CreateTournamentScreen

########## Start Screen ##########

class StartScreen(Screen):
	
	def __init__(self,name,screen_manager):
		
		super(StartScreen,self).__init__()
		self.name = name
		self.window_size = (300,300)	
		self.screen_manager = screen_manager

	def go_to_create_tournament(self):
		
		self.screen_manager.add_set(CreateTournamentScreen('create_tournament',self.screen_manager))
