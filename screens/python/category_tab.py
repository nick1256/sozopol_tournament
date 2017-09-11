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
from utilities.print import print_matches
from screens.python.problems_popup import ProblemsPopup
from screens.python.protocols_popup import ProtocolsPopup

# default row height
ROW_HEIGHT = 35

class CategoryTab(TabbedPanelItem):

	def __init__(self,database_name,category,**kwargs):
		
		super(CategoryTab,self).__init__(**kwargs)
		self.add_widget(CategoryContents(database_name,category))


class CategoryContents(GridLayout):
	
	def __init__(self,database_name,category,**kwargs):
	
		super(CategoryContents,self).__init__(**kwargs)

		self.database_name = database_name
		self.category=category
		
		# get round
		cnx = create_connection()
		cnx.database = self.database_name
		cursor = cnx.cursor()
		cursor.execute('select value from Variables where name=\"current_round_{}\"'.format(self.category))
		self.round = cursor.fetchall()[0][0]

		# get information for add protocols
		cursor.execute("select * from Matches_{} where day={};".format(self.category,self.round))
		self.locked = len(cursor.fetchall())!=0

		cnx.close()

		self.rows = 1

		self.left_widget   = CategoryButtons(size_hint_x = 0.1)
		self.middle_widget = CategoryTable(self,size_hint_x=0.45)
		self.right_widget  = MatchTable(self,size_hint_x = 0.45)

		self.add_widget(self.left_widget)
		self.add_widget(self.middle_widget)
		self.add_widget(self.right_widget)

		self.load()

	def load(self):

		# connect to database
		cnx = create_connection()
		cnx.database = self.database_name
		cursor = cnx.cursor()

		# get round
		cursor.execute('select value from Variables where name=\"current_round_{}\"'.format(self.category))
		self.round = cursor.fetchall()[0][0]

		# get information for set problems		
		cursor.execute("select * from Problems_{} where day={};".format(self.category,self.round))
		num_problems = len(cursor.fetchall())

		self.add_protocols_activate = False		
		self.finish_day_activate = False

		if num_problems == 0:
			self.set_problems_color = [1,0,0,1]
	
		elif num_problems < 8:
			self.set_problems_color = [1,1,0,1]

		elif num_problems == 8:
			self.set_problems_color = [0,1,0,1]
			self.add_protocols_activate = True
	
		# get information for add protocols
		cursor.execute("select * from Matches_{} where day={};".format(self.category,self.round))
		total = len(cursor.fetchall())
	
		cursor.execute("select * from Matches_{} where day={} and protocol_set=1;".format(self.category,self.round))
		done = len(cursor.fetchall())
	
		# close connection
		cnx.close()

		# locked and colors
		if total !=0:

			if done==0:
				self.add_protocols_color = [1,0,0,1]
			elif done!=total:
				self.add_protocols_color = [1,1,0,1]
			else:
				self.add_protocols_color = [0,1,0,1]
				self.finish_day_activate = True

		else:
			self.add_protocols_color = [1,1,1,1]

		# call widgets load method
		self.left_widget.load()
		self.middle_widget.load()
		self.right_widget.load()
		

	# generate the round
	def generate_round(self):
		
		# unlock
		self.unlock()	

		# actual work
		dname = self.database_name
		generate_round(dname,self.category,self.round)
		
		# visualisation
		self.right_widget.load()

	# locked mode
	def lock(self):
		self.locked = True
		self.right_widget.lock()
		self.load()

	# unlocked mode
	def unlock(self):
		self.locked = False
		self.right_widget.unlock()
		self.load()

	# set problems
	def set_problems(self):

		# get database
		dname = self.database_name		

		# make a popup for setting problems categories
		popup = Popup(background="utilities/blackgreen.jpg",title='Set Problems\' Categories',auto_dismiss=False,size_hint=(None,None),size=(800,800))
		popup.title_align = 'center'
		popup.title_size = '28sp'
		popup.content = ProblemsPopup(popup,self)
		popup.open()

	# add protocols
	def add_protocols(self):
		popup = Popup(background="utilities/blackgreen.jpg",title='Add Protocols',auto_dismiss=False,size_hint=(None,None),size=(800,800))
		popup.title_align = 'center'
		popup.title_size = '28sp'
		popup.content = ProtocolsPopup(popup,self)
		popup.open()

	# finish day
	def finish_day(self):
			
		# update round
		cnx = create_connection()
		cnx.database = self.database_name
		cursor = cnx.cursor()

		# go to next day
		cursor.execute('update Variables set value=value+1 where name=\"current_round_{}\"'.format(self.category))
	
		# commit and close		
		cnx.commit()	
		cnx.close()

		# reload
		self.unlock()
		self.load()

	# print matches
	def print_matches(self):

		# create connection		
		cnx = create_connection()
		cnx.database = self.database_name
		cursor = cnx.cursor()

		print_matches(cursor,self.category,self.round)


class CategoryTable(GridLayout):
		
	def __init__(self,parent_widget,**kwargs):

		super(CategoryTable,self).__init__(**kwargs)

		self.parent_widget = parent_widget

		# data
		self.database_name = parent_widget.database_name
		self.category = parent_widget.category
		self.round = parent_widget.round

		# connect to database
		cnx = create_connection()
		cnx.database = self.database_name
		cursor = cnx.cursor()

		cursor.execute("select value from Variables where name=\"number_teams_{}\";".format(self.category))
		nteams = cursor.fetchall()[0][0]
		self.nteams = int(nteams)

		# set grid		
		self.cols = 4
		self.padding = 50
		
		# draw first row:
		self.add_widget(BorderedLabel(size_hint = (1,None)  ,height=ROW_HEIGHT,text="Team Name"))	
		self.add_widget(BorderedLabel(size_hint = (0.5,None),height=ROW_HEIGHT,text="Rank Scores"))
		self.add_widget(BorderedLabel(size_hint = (0.5,None),height=ROW_HEIGHT,text="Points Diff."))
		self.add_widget(BorderedLabel(size_hint = (0.5,None),height=ROW_HEIGHT,text="Total Points"))

		# draw rest of the rows:

		self.widgets = []

		for row in range(self.nteams):
			widget_row = []

			widget_row.append(BorderedLabel(size_hint=(1,None),height=ROW_HEIGHT))
			widget_row.append(BorderedLabel(size_hint=(0.5,None),height=ROW_HEIGHT))
			widget_row.append(BorderedLabel(size_hint=(0.5,None),height=ROW_HEIGHT))
			widget_row.append(BorderedLabel(size_hint=(0.5,None),height=ROW_HEIGHT))

			self.widgets.append(widget_row)

		for widget_row in self.widgets:
			for widget in widget_row: self.add_widget(widget)

		# close connection
		cnx.close()



	def load(self):

		self.round = self.parent_widget.round

		# connect to database
		cnx = create_connection()
		cnx.database = self.database_name
		cursor = cnx.cursor()
	
		cursor.execute("select hidden_name,rank_scores,points_diff,points from Teams_{} order by rank_scores desc,points_diff desc,points desc,hidden_name;".format(self.category))
		team_info = [result for result in cursor.fetchall()]

		for row_num in range(len(self.widgets)):
			for col_num in range(len(self.widgets[row_num])):
				self.widgets[row_num][col_num].text = str(team_info[row_num][col_num])

		# close connection
		cnx.close()

class MatchTable(GridLayout):
	
	def __init__(self,parent_widget,**kwargs):

		super(MatchTable,self).__init__(**kwargs)

		self.parent_widget = parent_widget		

		self.database_name = parent_widget.database_name
		self.category = parent_widget.category
		self.round = parent_widget.round

		### find number of teams and team names
		# connect to database
		cnx = create_connection()
		cnx.database = self.database_name
		cursor = cnx.cursor()
	
		cursor.execute("select value from Variables where name=\"number_teams_{}\";".format(self.category))
		nteams = cursor.fetchall()[0][0]
		nteams = int(nteams)

		# close connection
		cnx.close()

		# set grid
		self.cols = 1

		self.padding = [10,10]
		self.spacing = [10,10]

		# indicate whether previous button was pressed
		self.pressed = 0

		# draw widgets
		self.nteams = nteams
		self.widgets = []

		for i in range(nteams//2):
			self.widgets.append((MatchWidget(i,size_hint_y=None,height=75)))

		if nteams%2:
			self.widgets.append((FreeWidget(size_hint_y=None,height=85)))

		for widget in self.widgets: self.add_widget(widget)

		for widget in self.widgets:	widget.lock()


	# swap labels
	def swap(self,button):
	
		if self.pressed==0:
			self.prev_button = button
			button.background_color = [0,1,0,1]

		else:
			self.prev_button.text, button.text = button.text , self.prev_button.text
			self.prev_button.background_color = [0,0,0,1]

		self.pressed = 1 - self.pressed


	def load(self):
	
		self.round = self.parent_widget.round

		for widget in self.widgets:
			widget.clear()

		# connect to database
		cnx = create_connection()
		cnx.database = self.database_name
		cursor = cnx.cursor()

		# get matches
		cursor.execute("select * from Matches_{} where day={};".format(self.category,self.round))
		matches = cursor.fetchall()
	
		#close connection
		cnx.close()

		# if no matches found, continue
		if len(matches)==0: return

		# assining names
		num=0

		for match in matches:

			team_one = match[0]
			team_two = match[1]

			jury_one = match[3]
			jury_two = match[4]

			if team_one == team_two:
				free_team = team_one
				continue

			self.widgets[num].set_button("button_left",team_one)
			self.widgets[num].set_button("button_right",team_two)		
			self.widgets[num].set_button("button_top",jury_one)
	
			if jury_two!="Null":
				self.widgets[num].set_button("button_bottom",jury_two)
			
			num+=1

		# extra "free" widget if odd number of teams
		if self.nteams%2: 
			self.widgets[-1].set_button(free_team)

	# lock widgets
	def lock(self):
			
		# remove pressed button if it exists
		self.pressed = 0
		
		# connect to database
		cnx = create_connection()
		cnx.database = self.database_name
		cursor = cnx.cursor()

		# clear previous and create matches
		cursor.execute("delete from Matches_{} where day={};".format(self.category,self.round))
		cnx.commit()

		for widget in self.widgets:
			info = widget.lock()
			cursor.execute("insert into Matches_{} values (\"{}\",\"{}\",{},\"{}\",\"{}\",0)".format(self.category,info[0],info[1],self.round,info[2],info[3]))

		# commit and renew view
		cnx.commit()
		cnx.close()

	# unlock widgets
	def unlock(self):
	
		for widget in self.widgets:
			widget.unlock()


### drawing widgets ###
class MatchWidget(Widget):
	
	def __init__(self,pos,**kwargs):

		self.rect_width = 200
		self.rect_height = ROW_HEIGHT
		self.line_len = ROW_HEIGHT		

		super(MatchWidget,self).__init__(**kwargs)

	def clicked(self,button_id):
		self.parent.swap(self.ids[button_id])

	def set_button(self,button_id,name):
		self.ids[button_id].text = name

	def lock(self):

		for button_id in self.ids:
			self.ids[button_id].disabled = True

		t1 = self.ids.button_left.text
		t2 = self.ids.button_right.text
		j1 = self.ids.button_top.text
		j2 = self.ids.button_bottom.text
		return (t1,t2,j1,j2)

	def unlock(self):
		self.ids.button_left.disabled = False
		self.ids.button_right.disabled = False
		self.ids.button_top.disabled = False
		self.ids.button_bottom.disabled = False

	def clear(self):
		for button_id in self.ids:
			self.ids[button_id].text = ""

# extra widget for free team if odd number of teams
class FreeWidget(Widget):
	
	def __init__(self,**kwargs):

		self.rect_width = 200
		self.rect_height = ROW_HEIGHT
		self.line_len = ROW_HEIGHT		

		super(FreeWidget,self).__init__(**kwargs)


	def clicked(self):
		self.parent.swap(self.ids["button"])

	def set_button(self,name):
		self.ids.button.text=name

	def lock(self):
		self.ids.button.disabled = True
		t1 = self.ids.button.text		
		return(t1,t1,"","")

	def unlock(self):
		self.ids.button.disabled = False
		
	def clear(self):
		self.ids.button.text = ""


class CategoryButtons(GridLayout):

	def __init__(self,**kwargs):

		super(CategoryButtons,self).__init__(**kwargs)

		self.cols = 1

		self.padding = [10,100]
		self.spacing = 10

		self.round_label = BorderedLabel(size_hint_y=None,height=ROW_HEIGHT)
		self.add_widget(self.round_label)	
	
		self.set_problems_button = Button(text="Set Problems",size_hint_y=None,height=ROW_HEIGHT,on_press=(lambda x: self.set_problems()))
		self.add_widget(self.set_problems_button)
		
		self.add_protocols_button = Button(text="Add Protocols",size_hint_y=None,height=ROW_HEIGHT,on_press=(lambda x: self.add_protocols()))
		self.add_widget(self.add_protocols_button)
	
		self.finish_day_button = Button(text="Finish Day",size_hint_y=None,height=ROW_HEIGHT,on_press=(lambda x: self.finish_day()))
		self.add_widget(self.finish_day_button)

		self.print_button = Button(text="Print Matches",size_hint_y=None,height=ROW_HEIGHT,on_press=(lambda x: self.print_matches()))
		self.add_widget(self.print_button)

		# add more spacing
		for i in range(10):
			self.add_widget(Label(text="",size_hint_y=None,height=ROW_HEIGHT))

		
		# buttons manipulating the round generation
		self.generate_button = Button(text="Generate Round",size_hint_y=None,height=ROW_HEIGHT,on_press=(lambda x: self.generate_round()))
		self.add_widget(self.generate_button)

		self.locked_button = Button(text="Lock Round",size_hint_y=None,height=ROW_HEIGHT,on_press=(lambda x: self.lock()))
		self.add_widget(self.locked_button)	

		self.unlocked_button = Button(text="Unlock Round",size_hint_y=None,height=ROW_HEIGHT,on_press=(lambda x: self.unlock()))
		self.add_widget(self.unlocked_button)


	# butons functions. call respective functions of parent
	def generate_round(self):
		self.parent.generate_round()

	def print_matches(self):
		self.parent.print_matches()

	def lock(self):
		self.parent.lock()

	def unlock(self):
		self.parent.unlock()

	def set_problems(self):
		self.parent.set_problems()

	def add_protocols(self):
		self.parent.add_protocols()

	def finish_day(self):
		self.parent.finish_day()

	# initial load
	def load(self):
		
		if self.parent.locked:
			self.unlocked_button.disabled=False
			self.print_button.disabled = False
			self.locked_button.disabled=True
			self.generate_button.disabled=True
		else:
			self.unlocked_button.disabled=True
			self.print_button.disabled=True			
			self.locked_button.disabled=False
			self.generate_button.disabled=False

		self.round_label.text = "Current Round: {}".format(self.parent.round)
		self.set_problems_button.background_color  = self.parent.set_problems_color
		self.add_protocols_button.disabled = not (self.parent.locked and self.parent.add_protocols_activate)
		self.add_protocols_button.background_color = self.parent.add_protocols_color
		self.finish_day_button.disabled = not (self.parent.locked and self.parent.finish_day_activate)

# bordering
class Bordered():
	pass

class BorderedLabel(Bordered,Label):
	pass

class BorderedButton(Bordered,Button):
	pass
