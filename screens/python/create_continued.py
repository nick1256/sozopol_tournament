# kivy imports
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.lang import Builder

# file imports
from screens.python.successful import SuccessfulCreateScreen

# mysql imports
import mysql.connector as mysqlc
from mysql.connector import errorcode

######### Abstract Create Continued Screen ########## 

class CreateContinuedScreen(Screen):

	
	def __init__(self,name,screen_manager,nteams):
		
		super(CreateContinuedScreen,self).__init__()
		self.name = name
		self.screen_manager = screen_manager		
		self.nteams = nteams
		
		# adjust screen to fit (8<=nteams<=16)		
		self.window_size = (800,200+50*nteams)

		# add layout
		self.add_widget(CustomLayout(self))

	# set text inputs
	def set_text_inputs(self,text_inputs):
		self.text_inputs = text_inputs

	# go to previous screen
	def go_back(self):
		self.screen_manager.set(self.back_screen_name)

	# get names and go to next screen
	def go_next(self):
		self.team_names = [text_input.text for text_input in self.text_inputs]
		self.screen_manager.set(self.next_screen_name)


######### Concrete Classes ##########

class CreateContinuedScreenSmall(CreateContinuedScreen):
	
	def __init__(self,name,screen_manager,nteams):
		
		self.label_text = "Insert Team Names for Group 6-7 (Step 2/4)"
		self.back_screen_name = "create_tournament"
		self.next_screen_name = "create_continued_medium"

		super(CreateContinuedScreenSmall,self).__init__(name,screen_manager,nteams)		


class CreateContinuedScreenMedium(CreateContinuedScreen):
	
	def __init__(self,name,screen_manager,nteams):
		
		self.label_text = "Insert Team Names for Group 8-9 (Step 3/4)"
		self.back_screen_name = "create_continued_small"
		self.next_screen_name = "create_continued_big"

		super(CreateContinuedScreenMedium,self).__init__(name,screen_manager,nteams)
		

class CreateContinuedScreenBig(CreateContinuedScreen):
	
	def __init__(self,name,screen_manager,nteams):
		
		self.label_text = "Insert Team Names for Group 10-12 (Step 4/4)"
		self.back_screen_name = "create_continued_medium"
		self.next_screen_name = "successful"

		super(CreateContinuedScreenBig,self).__init__(name,screen_manager,nteams)

	# override going to next screen to invoke creating database	
	def go_next(self):

		# get inputs
		self.team_names = [text_input.text for text_input in self.text_inputs]
		
		# get create_tournament screen and call it's create_database method
		target_screen = self.screen_manager.get_my_screen("create_tournament")		
		target_screen.create_database()

		#create next screen and go to it
		self.screen_manager.add_set(SuccessfulCreateScreen("successful",self.screen_manager))
		
### need to define Layout here because kivy doesn't have a for loop for nteams
class CustomLayout(GridLayout):
	
	def __init__(self,screen,**kwargs):

		GridLayout.__init__(self,**kwargs)
				
		self.rows = 3
		self.cols = 1


		label = Label(text=screen.label_text,size_hint_y=0.1)

		# table in the middle
		table = TableWidget(screen,size_hint_y=0.8)

		# buttons at the bottom	
		buttons = PairButtonWidget(screen,size_hint_y=0.1)

		# combine layout
		self.add_widget(label)
		self.add_widget(table)
		self.add_widget(buttons)


# table in the middle
class TableWidget(GridLayout):
	
	def __init__(self,screen,**kwargs):
		
		super(TableWidget,self).__init__(**kwargs)

		self.rows = screen.nteams
		self.cols = 2

		self.padding= [50,10,100,10]
		self.spacing = 10

		# list to hold the text of the text inputs
		text_inputs = []

		# create rows
		for row in range(self.rows):
		
			label = Label(text = "Team {} Name:".format(row+1),size_hint_x=0.3)
			text_input = TextInput(size_hint_x = 0.7,size_hint_y=None,height='32dp',font_size='11sp',write_tab=False,text="Team {}".format(row+1))
	
			# record text_input
			text_inputs.append(text_input)			
		
			# build the widget
			self.add_widget(label)
			self.add_widget(text_input)

		# set screen text inputs
		screen.set_text_inputs(text_inputs)



# buttons at the bottom
class PairButtonWidget(GridLayout):
		
	def __init__(self,screen,**kwargs):

		super(PairButtonWidget,self).__init__(**kwargs)
		self.screen = screen
	
		self.rows = 1
		self.cols = 2
		self.padding = 10
		self.spacing = 10

		# create the two buttons
		b1 = Button(text="Back",background_color = [1,0,0,1], on_press = (lambda x: screen.go_back()))
		b2 = Button(text="Create",background_color=[0,0,1,1], on_press = (lambda x: screen.go_next()))		

		# build the widget	
		self.add_widget(b1)
		self.add_widget(b2)	

