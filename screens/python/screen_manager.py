from kivy.uix.screenmanager import Screen,ScreenManager
from kivy.core.window import Window

class MyScreenManager(ScreenManager):
	
	def __init__(self):
		super(MyScreenManager,self).__init__()
		self.screens_dict = {}	

	def add(self,screen):
		self.add_widget(screen)
		self.screens_dict[screen.name] = screen
	
	def set(self,screen_name):
		self.current = screen_name
		screen = self.screens_dict[screen_name]
		Window.size = screen.window_size
