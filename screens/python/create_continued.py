# kivy imports
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.lang import Builder


# mysql imports
import mysql.connector as mysqlc
from mysql.connector import errorcode
from utilities.main_setup import setup_database

########## Create Continued Screen ########## 

class CreateContinuedScreen(Screen):

	
	def __init__(self,name,screen_manager,nteams,nrounds,tname):
		
		super(CreateContinuedScreen,self).__init__()
		self.name = name
		self.screen_manager = screen_manager		
		self.nteams = nteams
		self.nrounds = nrounds
		self.tname = tname
		self.tnames1 = None
		self.tnames2 = None
		
		# adjust screen to fit (8<=nteams<=16)		
		self.window_size = (800,200+50*nteams)
		
		# layout
		self.add_widget(CustomLayout(self))


	def set_text_inputs(self,text_inputs):
		self.text_inputs = text_inputs

	def create_database(self):

		# see where to go next according to which screen we are in
		if self.name=="create_continued_6-7":
			self.screen_manager.set("create_continued_8-9")
			next_screen = self.screen_manager.get_curr_screen()			
			tnames1 = [text_input.text for text_input in self.text_inputs]
			next_screen.tnames1 = tnames1

		elif self.name=="create_continued_8-9":
			self.screen_manager.set("create_continued_10-12")
			next_screen = self.screen_manager.get_curr_screen()
			tnames2 = [text_input.text for text_input in self.text_inputs]
			next_screen.tnames1 = self.tnames1
			next_screen.tnames2 = tnames2

		else:
			self.screen_manager.set("start")
			tnames3 = [text_input.text for text_input in self.text_inputs]
			
			# create database
			setup_database(self.tname,self.tnames1,self.tnames2,tnames3)


### need to define Layout here because kivy doesn't have a for loop for nteams
class CustomLayout(GridLayout):
	
	def __init__(self,screen,**kwargs):

		GridLayout.__init__(self,**kwargs)
				
		self.rows = 3
		self.cols = 1

	
		# upper label according to which screen we are on
		if screen.name=="create_continued_6-7":
			label_text = "Insert Team Names for Group 6-7 (Step 2/4)"

		elif screen.name=="create_continued_8-9":
			label_text = "Insert Team Names, Group 8-9 (Step 3/4)"

		else:
			label_text = "Insert Team Names, Group 10-12 (Steo 4/4)"

		label = Label(text=label_text,size_hint_y=0.1)

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
			text_input = TextInput(size_hint_x = 0.7,size_hint_y=None,height='32dp',font_size='12sp',write_tab=False)
	
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

		self.rows = 1
		self.cols = 2
		self.padding = 10
		self.spacing = 10

	
		# back screen name according to which screen we are on
		if screen.name=="create_continued_6-7":
			back_screen_name = "create_tournament"

		elif screen.name=="create_continued_8-9":
			back_screen_name = "create_continued_6-7"

		else:
			back_screen_name = "create_continued_8-9"

		# create the two buttons
		b1 = Button(text="Back",background_color = [1,0,0,1], on_press = (lambda x: screen.screen_manager.set(back_screen_name)))
		b2 = Button(text="Create",background_color=[0,0,1,1], on_press = (lambda x: screen.create_database()))		

		# build the widget	
		self.add_widget(b1)
		self.add_widget(b2)	


