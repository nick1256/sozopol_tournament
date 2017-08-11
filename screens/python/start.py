from kivy.uix.screenmanager import Screen
from screens.python.utilities import go_to_window

########## Start Screen ##########

class StartScreen(Screen):
	
	def __init__(self,name,screen_manager):
		
		super(StartScreen,self).__init__()
		self.name = name
		self.window_size = (300,300)	
		self.screen_manager = screen_manager

