# kivy imports
from kivy.uix.tabbedpanel import TabbedPanelItem
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout

# mysql imports
import mysql.connector as mysqlc
from mysql.connector import errorcode

# file imports
from utilities.create_connection import create_connection
from utilities.inserters import insert_people

# default row_height
ROW_HEIGHT = 30

# tab name with contents
class TeamsTab(TabbedPanelItem):

	def __init__(self,database_name,**kwargs):
		
		super(TeamsTab,self).__init__(**kwargs)
		self.add_widget(TeamsView(database_name))

class TeamsView(GridLayout):

	def __init__(self,database_name,**kwargs):

		super(TeamsView,self).__init__()
		self.database_name = database_name


		self.rows = 1
		self.cols = 3

		self.spacing = 20

		# left side with buttons
		self.left_side = TeamsButtons(size_hint_x = 0.1)

		# middle side with names of teams
		self.middle = TeamsSelection(database_name,size_hint_x = 0.2)

		# right side with members of the team
		self.right_side = PeopleView(size_hint_x = 0.7)

		#add widgets
		self.add_widget(self.left_side)
		self.add_widget(self.middle)
		self.add_widget(self.right_side)

	def show_category(self,category):

		# clean right side
		self.right_side.clean()

		self.category = category
		self.middle.show_category(category)

	def show_team(self,team):
		self.curr_team = team
		self.right_side.show_team(team)

	def select_category_button(self,category):
		self.left_side.select_button(category)

	def select_team_button(self,team):
		self.middle.select_button(team)


# buttons (left side)
class TeamsButtons(GridLayout):
	
	def __init__(self,**kwargs):

		super(TeamsButtons,self).__init__(**kwargs)

		self.rows = 3
		self.cols = 1

		self.padding = [10,100]
		self.spacing = 10

		# create dictionary for buttons
		self.buttons = {}

		self.buttons["Small"]  = Button(text="Teams 6-7",  size_hint_y=None,height=ROW_HEIGHT,on_press=(lambda x: self.parent.show_category("Small")))
		self.buttons["Medium"] = Button(text="Teams 8-9",  size_hint_y=None,height=ROW_HEIGHT,on_press=(lambda x: self.parent.show_category("Medium")))
		self.buttons["Big"]    = Button(text="Teams 10-12",size_hint_y=None,height=ROW_HEIGHT,on_press=(lambda x: self.parent.show_category("Big")))
	
		# draw widgets
		for button_text in sorted(self.buttons,reverse=True): self.add_widget(self.buttons[button_text])

	def select_button(self,category):

		# clear previous colors
		for button_name in self.buttons:
			self.buttons[button_name].background_color = [1,1,1,1]

		# select new category button
		self.buttons[category].background_color = [0,0,1,1]


# team names buttons (middle)
class TeamsSelection(GridLayout):
		
	def __init__(self,database_name,**kwargs):

		super(TeamsSelection,self).__init__(**kwargs)
		self.database_name = database_name

	def show_category(self,category):

		# color for selected category button
		self.parent.select_category_button(category)

		# clear previous widgets
		self.clear_widgets(self.children)

		# connect to database
		cnx = create_connection()
		cnx.database = self.database_name
		cursor = cnx.cursor()
	
		# get teams
		cursor.execute("select visible_name from Teams_{};".format(category))
		teams = [result[0] for result in cursor.fetchall()]

		# set number of rows to trigger the gridlayout
		self.rows = len(teams)
		self.padding = [10,50]
		self.spacing = 10

		# create dictionary for buttons
		self.buttons = {}

		for team in teams:
			self.buttons[team] = TeamButton(text=team,size_hint_y=None,height=ROW_HEIGHT) 

		# draw widgets
		for button_text in sorted(self.buttons): self.add_widget(self.buttons[button_text])
	
	def select_button(self,team):

		# clear previous colors
		for button_name in self.buttons:
			self.buttons[button_name].background_color = [1,1,1,1]

		# select new team button
		self.buttons[team].background_color = [0,0,1,1]



# people in the team (right side)
class PeopleView(GridLayout):

	def show_team(self,team):
	
		# select team button
		self.parent.select_team_button(team)

		# clear previous widgets if any
		self.clear_widgets(self.children)

		self.cols = 1

		self.padding = [50,50]
		self.spacing = 20

		self.widgets = []

		# draw header 
		self.header = PeopleHeader(size_hint_y=None,height=ROW_HEIGHT)
		self.widgets.append(self.header)

		### load people in that team
		
		# connect to database
		cnx = create_connection()
		cnx.database = self.parent.database_name
		cursor = cnx.cursor()

		# get information
		category = self.parent.category
		team = self.parent.curr_team

		query = "select name,alg_scores,comb_scores,geom_scores,num_scores,total_scores from People_{} where team=\"{}\" order by name;".format(category,team)
		cursor.execute(query)
	
		# add widgets for loaded people
		for result in cursor.fetchall():
			self.widgets.append(PeopleRow(result,size_hint_y=None,height=ROW_HEIGHT))

		# add buttons 
		self.buttons = PeopleButtons()
		self.widgets.append(self.buttons)

		# draw widgets
		for widget in self.widgets: self.add_widget(widget)

	def add_person(self):
	
		# remove buttons
		self.clear_widgets([self.buttons])
		self.widgets.pop()

		# add person row
		person = PeopleRow(size_hint_y=None,height=ROW_HEIGHT)
		self.add_widget(person)		
		self.widgets.append(person)

		# add buttons
		self.add_widget(self.buttons)		
		self.widgets.append(self.buttons)
		

	def save(self):

		# widgets that represent people
		people_rows = self.widgets[1:-1]

		# extract info
		people = []
		for people_row in people_rows:
			person = people_row.get_person()
			if person[0]!="": people.append(person) 

		# insert team name into each row and 
		for person in people:
			person.insert(1,self.parent.curr_team)


		### commit data to database

		# connect to database
		cnx = create_connection()
		cnx.database = self.parent.database_name
		cursor = cnx.cursor()

		# truncate previous records
		cursor.execute("delete from People_{} where team=\"{}\";".format(self.parent.category,self.parent.curr_team))
		
		# insert information
		insert_people(cursor,self.parent.category,people)

		# commit and close
		cnx.commit()
		cnx.close()
		
		self.show_team(self.parent.curr_team)

	def clean(self):
		self.clear_widgets(self.children)


class PeopleHeader(GridLayout):
	
	def __init__(self,**kwargs):

		super(PeopleHeader,self).__init__(**kwargs)

		self.cols = 6

		self.add_widget(BorderedLabel(text="Name",size_hint_x=0.5))
		self.add_widget(BorderedLabel(text="Alg. Sc.",size_hint_x=0.1))
		self.add_widget(BorderedLabel(text="Comb. Sc.",size_hint_x=0.1))
		self.add_widget(BorderedLabel(text="Geom. Sc.",size_hint_x=0.1))
		self.add_widget(BorderedLabel(text="Num. Sc.",size_hint_x=0.1))
		self.add_widget(BorderedLabel(text="Total Sc.",size_hint_x=0.1))



class PeopleRow(GridLayout):

	def __init__(self,loaded=None,**kwargs):
		
		super(PeopleRow,self).__init__(**kwargs)

		self.rows = 1

		self.widgets = []

		# add widgets
		if not loaded:
			self.widgets.append(TextInput(size_hint_x=0.5,multiline=False,on_text_validate=(lambda x: self.commit_person())))
		
			for num in range(5):
				self.widgets.append(BorderedLabel(text="0",size_hint_x=0.1))
		
		else:
			self.widgets.append(BorderedLabel(size_hint_x=0.5,text=loaded[0]))		
		
			for num in range(5):
				self.widgets.append(BorderedLabel(text=str(loaded[num+1]),size_hint_x=0.1))


		# draw widgets
		for widget in self.widgets : self.add_widget(widget)

	# transform text input to label
	def commit_person(self):

		# change first to label
		self.widgets[0] = BorderedLabel(text=self.widgets[0].text,size_hint_x=0.5)
		
		# clear and redraw
		self.clear_widgets(self.children)
		for widget in self.widgets: self.add_widget(widget)

	# get information for a person
	def get_person(self):

		info = []		
		for i in range(2):
			info.append(self.widgets[i].text)

		return info


class PeopleButtons(GridLayout):

	def __init__(self,**kwargs):
	
		super(PeopleButtons,self).__init__(**kwargs)
	
		self.cols = 2
		self.spacing = 50
		self.add_widget(Button(text="Add Person",size_hint=(None,None),height=ROW_HEIGHT,on_press = (lambda x: self.add_person()))) 
		self.add_widget(Button(text="Save Changes",size_hint=(None,None),height=ROW_HEIGHT,on_press = (lambda x: self.save())))

	def add_person(self):
		self.parent.add_person()

	def save(self):
		self.parent.save()
		


class Bordered():
	pass

class BorderedLabel(Bordered,Label):
	pass

class TeamButton(Button):
	def __init__(self,**kwargs):
		super(TeamButton,self).__init__(**kwargs)
		self.on_press = (lambda : self.parent.parent.show_team(self.text))


