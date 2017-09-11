""" Create continued Screen """

# kivy imports
from kivy.uix.screenmanager import Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

# file imports
# pylint: disable=E0401
from screens.python.successful import SuccessfulCreateScreen

class CreateContinuedScreen(Screen):
	""" Abstract Create Continued Screen """

	def __init__(self, name, screen_manager, nteams):

		super(CreateContinuedScreen, self).__init__()
		self.name = name
		self.screen_manager = screen_manager
		self.nteams = nteams

		self.team_names = None
		self.text_inputs = None

		# adjust screen to fit (8<=nteams<=16)
		self.window_size = (800, 200+50*nteams)

		# add layout
		self.add_widget(CustomLayout(self))

	def set_text_inputs(self, text_inputs):
		""" set text inputs """
		self.text_inputs = text_inputs

	def go_back(self):
		""" go to previous screen """
		self.screen_manager.set(self.back_screen_name)

	def go_next(self):
		""" get names and go to next screen"""
		self.team_names = [text_input.text for text_input in self.text_inputs]
		self.screen_manager.set(self.next_screen_name)


######### Concrete Classes ##########

class CreateContinuedScreenSmall(CreateContinuedScreen):

	""" For Small Group """

	def __init__(self, name, screen_manager, nteams):

		self.label_text = "Insert Team Names for Group 6-7 (Step 2/4)"
		self.back_screen_name = "create_tournament"
		self.next_screen_name = "create_continued_medium"

		super(CreateContinuedScreenSmall, self).__init__(name, screen_manager, nteams)


class CreateContinuedScreenMedium(CreateContinuedScreen):

	""" For Medium Group """

	def __init__(self, name, screen_manager, nteams):

		self.label_text = "Insert Team Names for Group 8-9 (Step 3/4)"
		self.back_screen_name = "create_continued_small"
		self.next_screen_name = "create_continued_big"

		super(CreateContinuedScreenMedium, self).__init__(name, screen_manager, nteams)


class CreateContinuedScreenBig(CreateContinuedScreen):

	""" For Big Group """

	def __init__(self, name, screen_manager, nteams):

		self.label_text = "Insert Team Names for Group 10-12 (Step 4/4)"
		self.back_screen_name = "create_continued_medium"
		self.next_screen_name = "successful"

		super(CreateContinuedScreenBig, self).__init__(name, screen_manager, nteams)

	def go_next(self):
		""" override going to next screen to invoke creating database """

		# get inputs
		self.team_names = [text_input.text for text_input in self.text_inputs]

		# get create_tournament screen and call it's create_database method
		target_screen = self.screen_manager.get_my_screen("create_tournament")
		target_screen.create_database()

		#create next screen and go to it
		self.screen_manager.add_set(SuccessfulCreateScreen("successful", self.screen_manager))


class CustomLayout(GridLayout):
	""" need to define Layout here because kivy doesn't have a for loop for nteams """

	def __init__(self, screen, **kwargs):

		GridLayout.__init__(self, **kwargs)

		self.rows = 3
		self.cols = 1


		label = Label(text=screen.label_text, size_hint_y=0.1)

		# table in the middle
		table = TableWidget(screen, size_hint_y=0.8)

		# buttons at the bottom
		buttons = PairButtonWidget(screen, size_hint_y=0.1)

		# combine layout
		self.add_widget(label)
		self.add_widget(table)
		self.add_widget(buttons)



class TableWidget(GridLayout):
	"""	table in the middle """

	def __init__(self, screen, **kwargs):

		super(TableWidget, self).__init__(**kwargs)

		self.rows = screen.nteams
		self.cols = 2

		self.padding = [50, 10, 100, 10]
		self.spacing = 10

		# list to hold the text of the text inputs
		text_inputs = []

		# create rows
		for row in range(self.rows):

			label = Label(text="Team {} Name:".format(row+1), size_hint_x=0.3)
			text_input = TextInput(size_hint_x=0.7, size_hint_y=None, height='32dp', font_size='11sp', write_tab=False)

			# record text_input
			text_inputs.append(text_input)

			# build the widget
			self.add_widget(label)
			self.add_widget(text_input)

		# set screen text inputs
		screen.set_text_inputs(text_inputs)



class PairButtonWidget(GridLayout):
	""" # buttons at the bottom """

	def __init__(self, screen, **kwargs):

		super(PairButtonWidget, self).__init__(**kwargs)
		self.screen = screen

		self.rows = 1
		self.cols = 2
		self.padding = 10
		self.spacing = 10

		# create the two buttons
		but1 = Button(text="Back", background_color=[1, 0, 0, 1], on_press=(lambda x: screen.go_back()))
		but2 = Button(text="Create", background_color=[0, 0, 1, 1], on_press=(lambda x: screen.go_next()))

		# build the widget
		self.add_widget(but1)
		self.add_widget(but2)
