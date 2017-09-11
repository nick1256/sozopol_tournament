""" Start Screen """

# kivy imports
from kivy.uix.screenmanager import Screen

# file imports
# pylint: disable=E0401
from screens.python.create_tournament import CreateTournamentScreen
from screens.python.load import LoadScreen

class StartScreen(Screen):

	""" Creates layout for starting page"""

	def __init__(self, name, screen_manager):

		super(StartScreen, self).__init__()
		self.name = name
		self.window_size = (250, 200)
		self.screen_manager = screen_manager

	def go_to_create_tournament(self):

		""" go to create tournament screen """

		self.screen_manager.add_set(CreateTournamentScreen('create_tournament', self.screen_manager))

	def load_tournament(self):

		""" go to loading"""

		self.screen_manager.add_set(LoadScreen('load', self.screen_manager))
