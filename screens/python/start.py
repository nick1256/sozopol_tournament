# kivy imports
from kivy.uix.screenmanager import Screen

# file imports
from screens.python.create_tournament import CreateTournamentScreen
from screens.python.load import LoadScreen
from screens.python.successful import SuccessfulLoadScreen

########## Start Screen ##########

class StartScreen(Screen):
	
	def __init__(self,name,screen_manager):
		
		super(StartScreen,self).__init__()
		self.name = name
		self.window_size = (250,200)	
		self.screen_manager = screen_manager

	def go_to_create_tournament(self):
		
		self.screen_manager.add_set(CreateTournamentScreen('create_tournament',self.screen_manager))

	def load_tournament(self):

		self.screen_manager.add_set(LoadScreen('load',self.screen_manager))
