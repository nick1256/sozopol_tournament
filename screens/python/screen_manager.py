from kivy.uix.screenmanager import Screen,ScreenManager
from kivy.core.window import Window
from screens.python.start import StartScreen

class MyScreenManager(ScreenManager):
	
	def __init__(self):
		
		# parent init
		super(MyScreenManager,self).__init__()
		
		# dictionary for available screens
		self.screens_dict = {}	

		# initialize with start screen
		self.add_set(StartScreen("start",self))

	# add a screen to the screen manager
	def add(self,screen):
		
		# if already exists in screen manager
		# remove and add updated
		if screen.name in self.screens_dict:
			self.remove_widget(self.screens_dict[screen.name])

		self.add_widget(screen)
		self.screens_dict[screen.name] = screen
	
	# navigate to a screen
	def set(self,screen_name):
		
		self.current = screen_name
		screen = self.screens_dict[screen_name]
		
		# adjust screen size		
		Window.size = screen.window_size

	def get_curr_screen(self):
		
		return self.screens_dict[self.current]


	# add and navigate to a screen
	def add_set(self,screen):
		self.add(screen)
		self.set(screen.name)