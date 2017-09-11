"""creates tamplate with the main view after loading """
# kivy imports
from kivy.uix.screenmanager import Screen
from kivy.uix.tabbedpanel import TabbedPanel

# file imports
# pylint: disable=E0401
from screens.python.category_tab import CategoryTab
from screens.python.jury_tab import JuryTab
from screens.python.teams_tab import TeamsTab

class MainViewScreen(Screen):

	""" working class """

	def __init__(self, name, screen_manager):

		self.window_size = (1900, 1200)
		self.name = name
		super(MainViewScreen, self).__init__()

		database_name = screen_manager.database_name
		self.add_widget(MainViewLayout(database_name, do_default_tab=False))

class MainViewLayout(TabbedPanel):

	""" layout """

	def __init__(self, database_name, **kwargs):

		super(MainViewLayout, self).__init__(**kwargs)

		# set background to black
		self.background_color = [0, 0, 0, 0]

		# create tabs
		self.add_widget(CategoryTab(database_name, "Small", text="6-7"))
		self.add_widget(CategoryTab(database_name, "Medium", text="8-9"))
		self.add_widget(CategoryTab(database_name, "Big", text="10-12"))
		self.add_widget(JuryTab(database_name, text="Jury"))
		self.add_widget(TeamsTab(database_name, text="Teams"))
