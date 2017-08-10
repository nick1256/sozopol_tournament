from kivy.uix.screenmanager import Screen

########## Start Screen ##########

class StartScreen(Screen):
	
	def __init__(self,name):
		
		super(StartScreen,self).__init__()
		self.name = name
		self.window_size = (300,300)	


	def go_to_createtournament(self):
		go_to_window('createtournament')


