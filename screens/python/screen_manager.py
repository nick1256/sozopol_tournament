""" Screen Manager """

# pylint: disable=E0401
from kivy.uix.screenmanager import ScreenManager
from kivy.core.window import Window
from screens.python.start import StartScreen

class MyScreenManager(ScreenManager):

	""" Custom Screen Manager """

	def __init__(self):

		# parent init
		super(MyScreenManager, self).__init__()

		# dictionary for available screens
		self.screens_dict = {}

		# database name we are reffering to
		self.database_name = None

		# initialize with start screen
		self.add_set(StartScreen("start", self))

	def add(self, screen):

		""" add a screen to the screen manager """

		# if already exists in screen manager
		# remove and add updated
		if screen.name in self.screens_dict:
			self.remove_widget(self.screens_dict[screen.name])

		self.add_widget(screen)
		self.screens_dict[screen.name] = screen

	def set(self, screen_name):

		""" navigate to a screen """

		self.current = screen_name
		screen = self.screens_dict[screen_name]

		# adjust screen size
		Window.size = screen.window_size

	def get_my_screen(self, screen_name):

		""" get screen according to a name """

		return self.screens_dict[screen_name]


	def add_set(self, screen):
		""" add and navigate to a screen """
		self.add(screen)
		self.set(screen.name)

	def set_database_name(self, name):
		""" set the name of the database we are using """
		self.database_name = name
