"""loaded page"""

# kivy imports
from kivy.uix.screenmanager import Screen

# pylint: disable=E0401
# file imports
from screens.python.successful import SuccessfulLoadScreen

class LoadScreen(Screen):

	""" loaded page class """

	def __init__(self, name, screen_manager):

		self.name = name
		self.screen_manager = screen_manager
		self.window_size = (300, 300)

		super(LoadScreen, self).__init__()


	def load_tournament(self, selection):

		""" actually loading the tournament """

		# get name of tournament
		tname = selection.split("/")[-1]

		# if tournament was selected:
		if tname != "tournaments":

			# link database
			self.screen_manager.set_database_name(tname)

			self.screen_manager.add_set(SuccessfulLoadScreen("successful", self.screen_manager))
