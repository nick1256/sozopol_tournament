# kivy imports 
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.behaviors import ToggleButtonBehavior

# mysql imports
import mysql.connector as mysqlc
from mysql.connector import errorcode

# file imports
from utilities.create_connection import create_connection
from utilities.inserters import insert_problems

class ProblemsPopup(GridLayout):
	
	def __init__(self,popup,parent_widget,**kwargs):

		super(ProblemsPopup,self).__init__(**kwargs)
		self.popup = popup
		self.parent_widget = parent_widget

		self.rows = 9
		self.cols = 1

		self.spacing = 10
		self.padding = 10

		# add the 8 problems rows

		self.widgets = []

		for problem_num in range(8):
			self.widgets.append(ProblemsRow(str(problem_num+1)))

		# add buttons
		self.widgets.append(ProblemsButtons())

		# draw widgets
		for widget in self.widgets: self.add_widget(widget)

		# load init data
		self.load()


	def dismiss(self):
		self.popup.dismiss()

	def commit(self):

		problems = set()

		# find out the categories
		for num in range(8):
			button_group = ToggleButtonBehavior.get_widgets(str(num+1))
			for button in button_group:
				if button.state=="down": 
					problems.add(("Problem {}".format(num+1),button.text))

		# create connection
		cnx = create_connection()
		cnx.database = self.parent_widget.database_name
		cursor = cnx.cursor()

		# push data
		cursor.execute("delete from Problems_{} where day={};".format(self.parent_widget.category,self.parent_widget.round))
		insert_problems(cursor,self.parent_widget.category,self.parent_widget.round,problems)
		
		# commit and exit
		cnx.commit()
		cnx.close()		
		
		# exit popup and reload parent
		self.popup.dismiss()
		self.parent_widget.load()

	def load(self):

		self.round = self.parent_widget.round
		
		# create connection
		cnx = create_connection()
		cnx.database = self.parent_widget.database_name
		cursor = cnx.cursor()

		# get data				
		cursor.execute("select * from Problems_{} where day={};".format(self.parent_widget.category,self.round))
		problems_set = cursor.fetchall()

		# send to corresponding row
		for problem in problems_set:
			
			problem_num = int(problem[0].split(" ")[1])
			problem_category = problem[1]

			self.widgets[problem_num-1].set_loaded(problem_category)
	


class ProblemsRow(GridLayout):
	
	def __init__(self,number,**kwargs):
		
		super(ProblemsRow,self).__init__(**kwargs)

		self.rows = 1
		self.cols = 5

		self.spacing = 10
		self.padding = 10

		self.add_widget(Label(text="Problem {}:".format(number)))

		self.add_widget(ToggleButton(text="Alg.",group=number))
		self.add_widget(ToggleButton(text="Comb.",group=number))
		self.add_widget(ToggleButton(text="Geom.",group=number))
		self.add_widget(ToggleButton(text="Num.",group=number))

	def set_loaded(self,category):
		
		# check which button has the corresponding text
		
		for button in self.children:			
			if button.text == category:
				down_button = button

		down_button.state="down"


class ProblemsButtons(GridLayout):

	def __init__(self,**kwargs):
		
		super(ProblemsButtons,self).__init__(**kwargs)

		self.rows = 1
		self.cols = 2

		self.spacing = 100
		self.padding = [50,10]

		self.add_widget(Button(text="Back",background_color = [1,0,0,1],on_press=(lambda x: self.parent.dismiss())))
		self.add_widget(Button(text="Continue",background_color = [0,0,1,1],on_press=(lambda x: self.parent.commit())))
		



