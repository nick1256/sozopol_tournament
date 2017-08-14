# kivy imports
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.tabbedpanel import TabbedPanel

# file imports
from utilities.create_connection import create_connection
from screens.python.category_tab import CategoryTab
from screens.python.jury_tab import JuryTab

class MainViewScreen(Screen):
	
	def __init__(self,name,screen_manager):
		
		self.name = name
		self.screen_manager = screen_manager
		self.window_size = (1900,1000)
		
		super(MainViewScreen,self).__init__()

		self.add_widget(MainViewLayout(self,do_default_tab=False))


class MainViewLayout(TabbedPanel):
	
	def __init__(self,screen,**kwargs):
		
		super(MainViewLayout,self).__init__(**kwargs)

		# set background to black
		self.background_color = [0,0,0,0]

		# create the three tabs for the different categories
		self.add_widget(CategoryTab(screen,"Small",text="6-7"))
		self.add_widget(CategoryTab(screen,"Medium",text="8-9"))
		self.add_widget(CategoryTab(screen,"Big",text="10-12"))
		self.add_widget(JuryTab(screen,text="Jury"))



				



