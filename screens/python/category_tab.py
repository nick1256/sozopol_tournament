# kivy imports
from kivy.uix.tabbedpanel import TabbedPanelItem
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.popup import Popup

# mysql imports
import mysql.connector as mysqlc
from mysql.connector import errorcode

# file imports
from utilities.create_connection import create_connection
from utilities.generate_round import generate_round
from screens.python.problems_popup import ProblemsPopup


class CategoryTab(TabbedPanelItem):

	def __init__(self,screen,category,**kwargs):
		
		super(CategoryTab,self).__init__(**kwargs)
		self.add_widget(CategoryContents(screen,category))
		

class CategoryContents(GridLayout):
	
	def __init__(self,screen,category,**kwargs):
	
		super(CategoryContents,self).__init__(**kwargs)

		self.screen = screen		
		self.category=category
	
		self.rows = 1
		self.cols = 3

		self.left_widget   = CategoryButtons(screen,size_hint_x = 0.1)
		self.middle_widget = CategoryTable(screen,category,size_hint_x=0.5)
		self.right_widget  = MatchTable(screen,category,size_hint_x = 0.4)

		self.add_widget(self.left_widget)
		self.add_widget(self.middle_widget)
		self.add_widget(self.right_widget)

		self.locked = False
	

	# generate the round
	def generate_round(self):
		
		# actual work
		dname = self.screen.screen_manager.database_name
		generate_round(dname,self.category)
		
		# visualisation
		self.right_widget.show_round()

	# locked mode
	def lock(self):
		self.locked = True
		self.right_widget.lock()

	# unlocked mode
	def unlock(self):
		self.locked = False
		self.right_widget.unlock()

	
	def set_problems(self):
		
		# make a popup for setting problems categories
		popup = Popup(title='Set Problems\' Categories',auto_dismiss=False,size_hint=(None,None),size=(800,800))
		popup.content = ProblemsPopup(popup)
		popup.open()



class CategoryTable(GridLayout):
		
	def __init__(self,screen,category,**kwargs):

		super(CategoryTable,self).__init__(**kwargs)

		### get relevant information for number of teams from mysql ###

		# connect to database
		cnx = create_connection()
		cnx.database = screen.screen_manager.database_name
		cursor = cnx.cursor()

		# get information				
		cursor.execute("select value from Variables where name=\"number_rounds\";")
		nrounds = cursor.fetchall()[0][0]
		nrounds = int(nrounds)

		cursor.execute("select value from Variables where name=\"number_teams_{}\";".format(category))
		nteams = cursor.fetchall()[0][0]
		nteams = int(nteams)
		
		cursor.execute("select visible_name from Teams_{} order by rank_scores,points,visible_name;".format(category))
		team_names = [result[0] for result in cursor.fetchall()]

		# close connection
		cnx.close()

		# set grid		
		self.rows = nteams+1
		self.cols = nrounds+3
		self.padding = 50
		
		# draw first row:

		self.add_widget(BorderedLabel(size_hint_x=1))
		
		for col in range(nrounds):
			self.add_widget(BorderedLabel(size_hint_x = 0.5, text="Round {}".format(col+1)))
	
		self.add_widget(BorderedLabel(size_hint_x = 0.5, text="Scores"))
		self.add_widget(BorderedLabel(size_hint_x = 0.5, text="Points"))


		# draw rest of the rows:

		for row in range(nteams):
			self.add_widget(BorderedLabel(size_hint_x=1,text="{}".format(team_names[row])))

			for col in range(nrounds):
				self.add_widget(BorderedLabel(size_hint_x=0.5))

			self.add_widget(BorderedLabel(size_hint_x=0.5,text="0"))
			self.add_widget(BorderedLabel(size_hint_x=0.5,text="0"))


class MatchTable(GridLayout):
	
	def __init__(self,screen,category,**kwargs):

		super(MatchTable,self).__init__(**kwargs)

		### find number of teams and team names

		self.screen = screen
		self.category = category		

		# connect to database
		cnx = create_connection()
		cnx.database = screen.screen_manager.database_name
		cursor = cnx.cursor()
	
		cursor.execute("select value from Variables where name=\"number_teams_{}\";".format(category))
		nteams = cursor.fetchall()[0][0]
		nteams = int(nteams)


		# set grid
		self.cols = 1
		self.rows = (nteams+1)//2

		self.padding = [10,50]
		self.spacing = [10,10]
		self.pressed = 0

		# draw widgets
		self.nteams = nteams
		self.widgets = []

		for i in range(nteams//2):
			self.widgets.append((MatchWidget(i)))

		if nteams%2:
			self.widgets.append((FreeWidget()))

		for widget in self.widgets: self.add_widget(widget)
	
		# load matches data if available
		self.show_round()

	# swap labels
	def swap(self,button):
	
		if self.pressed==0:
			self.prev_button = button
			button.background_color = [0,1,0,1]

		else:
			self.prev_button.text, button.text = button.text , self.prev_button.text
			self.prev_button.background_color = [0,0,0,1]

		self.pressed = 1 - self.pressed

	# look at matches table in database and send names appropriately
	def show_round(self):

		
		# connect to database
		cnx = create_connection()
		cnx.database = self.screen.screen_manager.database_name
		cursor = cnx.cursor()

		# get matches
		cursor.execute("select * from Matches_{};".format(self.category))
		matches = cursor.fetchall()
	
		# assining names
		for num in range(self.nteams//2):

			team_one = matches[num][0]
			team_two = matches[num][1]

			self.widgets[num].set_button("button_left",team_one)
			self.widgets[num].set_button("button_right",team_two)
		
		# extra "free" widget if odd number of teams
		if self.nteams%2:
			self.widgets[-1].set_button(matches[-1][0])

	# lock widgets
	def lock(self):
	
		for widget in self.widgets:
			widget.lock()

	# unlock widgets
	def unlock(self):
	
		for widget in self.widgets:
			widget.unlock()


### drawing widgets ###
class MatchWidget(Widget):
	
	def __init__(self,pos,**kwargs):

		self.rect_width = 200
		self.rect_height = 40
		self.line_len = 50		

		super(MatchWidget,self).__init__(**kwargs)

	def clicked(self,button_id):
		self.parent.swap(self.ids[button_id])

	def set_button(self,button_id,name):
		self.ids[button_id].text = name

	def lock(self):
		self.ids.button_left.disabled = True
		self.ids.button_right.disabled = True
		self.ids.button_top.disabled = True
		self.ids.button_bottom.disabled = True

	def unlock(self):
		self.ids.button_left.disabled = False
		self.ids.button_right.disabled = False
		self.ids.button_top.disabled = False
		self.ids.button_bottom.disabled = False

# extra widget for free team if odd number of teams
class FreeWidget(Widget):
	
	def __init__(self,**kwargs):

		self.rect_width = 200
		self.rect_height = 40
		self.line_len = 50		

		super(FreeWidget,self).__init__(**kwargs)


	def clicked(self,button_id):
		self.parent.swap(self.ids[button_id])

	def set_button(self,name):
		self.ids.button.text=name

	def lock(self):
		self.ids.button.disabled = True	

	def unlock(self):
		self.ids.button.disabled = False

class CategoryButtons(GridLayout):

	def __init__(self,screen,**kwargs):

		super(CategoryButtons,self).__init__(**kwargs)

		self.rows = 4
		self.cols = 1

		self.screen = screen

		self.padding = [10,100]
		self.spacing = 10

		self.add_widget(Button(text="Generate Round",size_hint_y=None,height=40,on_press=(lambda x: self.generate_round())))
		self.add_widget(Button(text="Lock Day",size_hint_y=None,height=40,on_press=(lambda x: self.lock())))
		self.add_widget(Button(text="Unlock Day",size_hint_y=None,height=40,on_press=(lambda x: self.unlock())))
		self.add_widget(Button(text="Set Problems",size_hint_y=None,height=40,on_press=(lambda x: self.set_problems())))

	# butons functions. call respective functions of parent
	def generate_round(self):
		self.parent.generate_round()

	def lock(self):
		self.parent.lock()

	def unlock(self):
		self.parent.unlock()

	def set_problems(self):
		self.parent.set_problems()


# bordering
class Bordered():
	pass

class BorderedLabel(Bordered,Label):
	pass

class BorderedButton(Bordered,Button):
	pass

