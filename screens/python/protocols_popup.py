# kivy imports 
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.togglebutton import ToggleButton
from kivy.graphics import Color,Rectangle


# mysql imports
import mysql.connector as mysqlc
from mysql.connector import errorcode

# file imports
from utilities.create_connection import create_connection

# default row_height
ROW_HEIGHT = 40

class ProtocolsPopup(GridLayout):

	def __init__(self,popup,parent_widget,**kwargs):

		super(ProtocolsPopup,self).__init__(**kwargs)

		self.parent_widget = parent_widget

		self.popup = popup
		self.database_name = parent_widget.database_name
		self.category = parent_widget.category
		self.round = parent_widget.round


		# connect to database
		cnx = create_connection()
		cnx.database = self.database_name
		cursor = cnx.cursor()

		# get matches
		cursor.execute("select * from Matches_{} where day={};".format(self.category,self.round))
		matches = cursor.fetchall()

		# set table
		self.cols = 1
		self.rows = len(matches) + 1

		self.spacing = 10
		self.padding = 10

		self.widgets = []	
	
		# for ACTUAL matches (exclude free wins)
		for match in matches:

			if match[0]!=match[1]:
				self.widgets.append(ProtocolRow(self,match[0],match[1]))
		
		# free match
		for match in matches:
			if match[0]==match[1]:
				self.widgets.append(FreeRow(self,match[0]))


		# add buttons widget
		self.widgets.append(ProtocolButtons())

		# draw widgets
		for widget in self.widgets: self.add_widget(widget)

	def dismiss(self):
		self.popup.dismiss()

	def commit(self):
		self.parent_widget.load()
		self.popup.dismiss()


class ProtocolButtons(GridLayout):

	def __init__(self,**kwargs):

		super(ProtocolButtons,self).__init__(**kwargs)

		self.spacing = 100
		self.padding = [50,10]

		self.rows = 1
		self.cols = 2

		self.add_widget(Button(text="Back",background_color = [1,0,0,1],on_press=(lambda x: self.parent.dismiss())))
		self.add_widget(Button(text="Continue",background_color = [0,0,1,1],on_press=(lambda x: self.parent.commit())))


class FreeRow(GridLayout):

	def __init__(self,parent_widget,team,**kwargs):
		
		super(FreeRow,self).__init__(**kwargs)

		self.parent_widget = parent_widget

		self.database_name = parent_widget.database_name
		self.category = parent_widget.category
		self.round = parent_widget.round
		self.team = team

		# set grid
		self.cols = 4
		self.spacing = 10
		self.padding = 10

		# visuals
		self.add_widget(Label(text=team,size_hint_x = 0.3))
		self.add_widget(Label(text="gets",size_hint_x = 0.1))
		self.add_widget(Label(text="Free Win",size_hint_x = 0.3))
		self.add_widget(Button(text="Add Protocol",size_hint_x = 0.3,on_press=(lambda x: self.set())))
		
		# load initial state
		self.load()		


	def load(self):

		self.round = self.parent_widget.round
		
		# connect to database
		cnx = create_connection()
		cnx.database = self.database_name
		cursor = cnx.cursor()
								
		# find if this match protocol has been set
		query = "select protocol_set from Matches_{} where team_one=\"{}\" and team_two=\"{}\" and day={};".format(self.category,self.team,self.team,self.round)
		cursor.execute(query)
		result = cursor.fetchall()[0][0]

		if result:
			self.children[0].background_color = [0,1,0,1]
			self.children[0].disabled = True
		else:
			self.children[0].background_color = [1,0,0,1]
			

	def set(self):
	
		# connect to database
		cnx = create_connection()
		cnx.database = self.database_name
		cursor = cnx.cursor()

		query = "update Matches_{} set protocol_set=1 where team_one=\"{}\" and team_two=\"{}\" and day={}".format(self.category,self.team,self.team,self.round)
		cursor.execute(query)

		# give them 2 rank scores, 48 points and 0 point diff 
		cursor.execute("update Teams_{} set rank_scores=rank_scores+2, points=points+48 where hidden_name=\"{}\";".format(self.category,self.team))

		cnx.commit()
		cnx.close()			
	
		# reload
		self.load()



class ProtocolRow(GridLayout):
		
	def __init__(self,parent_widget,team_one,team_two,**kwargs):

		super(ProtocolRow,self).__init__(**kwargs)
		self.parent_widget = parent_widget

		self.database_name = parent_widget.database_name
		self.category = parent_widget.category
		self.round = parent_widget.round

		self.team_one = team_one
		self.team_two = team_two	

		self.rows = 1
		self.cols = 4

		self.spacing = 10
		self.padding = 10

		self.add_widget(Label(text=team_one,size_hint_x = 0.3))
		self.add_widget(Label(text="vs",size_hint_x = 0.1))
		self.add_widget(Label(text=team_two,size_hint_x = 0.3))
		self.add_widget(Button(text="Add Protocol",size_hint_x = 0.3,on_press=(lambda x: self.create_protocol())))

		# load 
		self.load()


	def load(self):
		
		self.round = self.parent_widget.round

		# connect to database
		cnx = create_connection()
		cnx.database = self.database_name
		cursor = cnx.cursor()
								
		# find if this match protocol has been set
		query = "select protocol_set from Matches_{} where team_one=\"{}\" and team_two=\"{}\" and day={};".format(self.category,self.team_one,self.team_two,self.round)
		cursor.execute(query)
		result = cursor.fetchall()[0][0]
	
		if result:
			self.children[0].background_color = [0,1,0,1]
			self.children[0].disabled = True
			self.children[0].text="Protocol Added"
		else:
			self.children[0].background_color = [1,0,0,1]


	def create_protocol(self):
		
		popup = Popup(background="utilities/blackgreen.jpg",auto_dismiss=False,size_hint=(None,None),size=(1500,1000))
		popup.title= self.team_one + "     vs.     " + self.team_two
		popup.title_align = 'center'
		popup.title_size = '28sp'
		popup.content = MatchPopup(popup,self)
		popup.open()

class MatchPopup(GridLayout):

	def __init__(self,popup,parent_widget,**kwargs):

		super(MatchPopup,self).__init__(**kwargs)
		self.popup = popup
		
		self.parent_widget = parent_widget
		self.database_name = parent_widget.database_name
		self.category = parent_widget.category
		self.round = parent_widget.round

		team_one = parent_widget.team_one
		team_two = parent_widget.team_two


		# draw grid
		self.cols = 3 
		self.spacing = 10
		self.padding = 20
		
		# add wdigets 
		self.middle     = MatchTable(self,team_one,team_two,size_hint = (0.7,0.9))
		self.left_side  = TeamSide(self,team_one,size_hint = (0.15,0.9))
		self.right_side = TeamSide(self,team_two,size_hint = (0.15,0.9))

		# draw widgets
		self.add_widget(self.left_side)
		self.add_widget(self.middle)
		self.add_widget(self.right_side)

		# add buttons for confirmation and back
		# add an empty widgets to adjust the buttons to the middle (grid shit)
		self.add_widget(Label(text="",size_hint = (0.15,0.1)))
		self.add_widget(MatchButtons(size_hint = (0.7,0.1)))
		self.add_widget(Label(text="",size_hint = (0.15,0.1)))

	def insert_value(self,value):
		self.middle.insert_value(value)

	def close(self):
		self.popup.dismiss()

	def commit(self):

		self.middle.commit_data()
		self.popup.dismiss()
		self.parent_widget.load()

class TeamSide(GridLayout):

	def __init__(self,parent_widget,team,**kwargs):
		
		super(TeamSide,self).__init__(**kwargs)

		self.parent_widget = parent_widget
		self.database_name = parent_widget.database_name
		self.category = parent_widget.category		

		self.cols = 1
		self.padding = [20,10]
		self.spacing = 10
	

		### find team members

		# connect to database
		cnx = create_connection()
		cnx.database = self.database_name
		cursor = cnx.cursor()

		# get people from team
		cursor.execute("select name from People_{} where team=\"{}\";".format(self.category,team))
		people = [result[0] for result in cursor.fetchall()]

		# draw buttons for each person
		self.add_widget(Label(text=team,font_size='22sp',size_hint_y=None,height=ROW_HEIGHT))

		# buttons for each person in the team
		for person in people:
			self.add_widget(ValueButton(self,text=person))	

		# add empty labels for spacing
		for num in range(7-len(people)):
			self.add_widget(Label(text=""))


		self.add_widget(NumPad(self,size_hint_y=None,height=300))

	# use button click to insert value into table
	def insert_value(self,value):
		self.parent_widget.insert_value(value)

# create 0-12 numpad for number entries
class NumPad(GridLayout):

	def __init__(self,parent,**kwargs):

		super(NumPad,self).__init__(**kwargs)
		self.parent_widget = parent		

		self.cols = 3
	
		# add numbers from 1 to 12
		for num_row in range(3,-1,-1):
			for num_col in range(1,4):
				self.add_widget(ValueButton(self,text=str(3*num_row+num_col)))

		# add 0
		self.add_widget(Label(size_hint_y=None,height=ROW_HEIGHT,text=""))
		self.add_widget(ValueButton(self,text="0"))
		self.add_widget(Label(size_hint_y=None,height=ROW_HEIGHT,text=""))

	# use button click to insert value into table
	def insert_value(self,value):
		self.parent_widget.insert_value(value)
		
# button whose press inserts value into table
class ValueButton(Button):

	def __init__(self,parent,**kwargs):

		super(ValueButton,self).__init__(**kwargs)
		self.size_hint_y=None
		self.height=ROW_HEIGHT
		self.on_press = (lambda : parent.insert_value(self.text))


# table for protocol
class MatchTable(GridLayout):

	def __init__(self,parent_widget,team_one,team_two,**kwargs):
		
		super(MatchTable,self).__init__(**kwargs)
		self.database_name = parent_widget.database_name
		self.category = parent_widget.category
		self.round = parent_widget.round
			
		self.team_one = team_one
		self.team_two = team_two	

		# one column per row
		self.cols = 1
	
		self.add_widget(MatchHeader(size_hint_y=None,height=ROW_HEIGHT))
		self.match_results = MatchResults(self) 	
		self.add_widget(self.match_results)

	def insert_value(self,value):
		self.match_results.insert_value(value)

	def commit_data(self):
		self.match_results.commit_data()

# header 
class MatchHeader(GridLayout):

	def __init__(self,**kwargs):

		super(MatchHeader,self).__init__(**kwargs)

		self.rows = 1

		self.add_widget(BorderedLabel(text="Pr. №",size_hint_x=0.0625))
		self.add_widget(BorderedLabel(text="Student",size_hint_x=0.25))
		self.add_widget(BorderedLabel(text="Score",size_hint_x=0.0625))
		self.add_widget(BorderedLabel(text="Direction",size_hint_x=0.25))
		self.add_widget(BorderedLabel(text="Student",size_hint_x=0.25))
		self.add_widget(BorderedLabel(text="Score",size_hint_x=0.0625))
		self.add_widget(BorderedLabel(text="Jury Sc.",size_hint_x=0.0625))


class MatchResults(GridLayout):	
	
	def __init__(self,parent_widget,**kwargs):

		super(MatchResults,self).__init__(**kwargs)

		self.database_name = parent_widget.database_name
		self.category = parent_widget.category
		self.round = parent_widget.round

		self.cols = 7
		
		# size_hints_x for widgets
		self.sizes = [0.0625,0.25,0.0625,0.25,0.25,0.0625,0.0625] 

		self.padding = [0,20]
		self.spacing = 3

		# curr position for input
		self.curr_pos = [0,0]

		# list of lists of widgets
		self.widgets = []

		# create widgets
		for i in range(8):
			widget_row = []

			# cycle through columns
			for j in range(self.cols):
				widget_row.append(BorderedLabel(size_hint=(self.sizes[j],None),height=ROW_HEIGHT))

			self.widgets.append(widget_row)				
			
		# change the direction to buttons
		for i in range(8):
			self.widgets[i][3] = DirectionRow(i,size_hint=(self.sizes[3],None),height=ROW_HEIGHT) 

		#activate first widget
		self.widgets[self.curr_pos[0]][self.curr_pos[1]] = ColoredLabel(size_hint=(self.sizes[0],None),height=ROW_HEIGHT)

		# buttons for navigation
		self.widgets.append([Label(text="",size_hint=(self.sizes[0],None),height=ROW_HEIGHT),NavigationButtons(size_hint_x=self.sizes[1])])

		# draw widgets
		for widget_row in self.widgets:
			for widget in widget_row:
				self.add_widget(widget)

	def insert_value(self,value):

		# insert value in current position and deactivate widget
		self.widgets[self.curr_pos[0]][self.curr_pos[1]].text = value
		self.widgets[self.curr_pos[0]][self.curr_pos[1]] = BorderedLabel(text=value,size_hint=(self.sizes[self.curr_pos[1]],None),height=ROW_HEIGHT)
		self.go_next()

	def redraw(self):
		
		#clear and redraw
		self.clear_widgets(self.children)
		for widget_row in self.widgets:
			for widget in widget_row:
				self.add_widget(widget)

	# remove blue border arround current position
	def deactivate(self):
		
		text = self.widgets[self.curr_pos[0]][self.curr_pos[1]].text 
		self.widgets[self.curr_pos[0]][self.curr_pos[1]] = BorderedLabel(text=text,size_hint=(self.sizes[self.curr_pos[1]],None),height=ROW_HEIGHT)
		self.redraw()

	# add blue border arround current position
	def activate(self):

		text = self.widgets[self.curr_pos[0]][self.curr_pos[1]].text 
		self.widgets[self.curr_pos[0]][self.curr_pos[1]] = ColoredLabel(text=text,size_hint=(self.sizes[self.curr_pos[1]],None),height=ROW_HEIGHT)
		self.redraw()

	# clear
	def clear(self):
		self.widgets[self.curr_pos[0]][self.curr_pos[1]].text=""

	# go to next position in table
	def go_next(self):
		
		if self.curr_pos == [7,6] : return

		self.deactivate()

		# go to next position
		if self.curr_pos[1]<6:
			# skip directions
			if self.curr_pos[1] == 2:
				self.curr_pos[1]+=2
			else:self.curr_pos[1]+=1
		# go to new row		
		else: 
			self.curr_pos[0]+=1
			self.curr_pos[1]=0

		self.activate()

	# go to prev position in table
	def go_prev(self):
		
		if self.curr_pos == [0,0] : return

		# deactivate previous selected
		self.deactivate()
		
		# go to prev position
		if self.curr_pos[1]>0:
			# skip directions
			if self.curr_pos[1] == 4:
				self.curr_pos[1]-=2
			else:self.curr_pos[1]-=1
		# go to prev row if needed		
		else: 
			self.curr_pos[0]-=1
			self.curr_pos[1]=6

		# select precious
		self.activate()

	# finish making changes in protocol
	def finish(self):

		# remove the navigation buttons
		self.widgets.pop()
		
		# remove selection and redraw
		self.deactivate()

		# add Final Results Line

		self.add_widget(Label(text="",size_hint=(self.sizes[0],None),height=ROW_HEIGHT))
		self.add_widget(Label(text="Final Results:",font_size='20sp',size_hint=(self.sizes[1],None),height=ROW_HEIGHT))		

		for i in range(2,7):
			self.add_widget(Label(size_hint=(self.sizes[i],None),height=ROW_HEIGHT))

		# get team names		
		team_one_name = self.parent.team_one
		team_two_name = self.parent.team_two

		# get points
		team_one_points = 0
		for i in range(8):
			if self.widgets[i][2].text!='':
				team_one_points+=int(self.widgets[i][2].text)
		
		team_two_points = 0
		for i in range(8):
			if self.widgets[i][5].text!='':
				team_two_points+=int(self.widgets[i][5].text)

		jury_points = 0
		for i in range(8):
			if self.widgets[i][6].text!='':
				jury_points+=int(self.widgets[i][6].text)

		# get outcome of the match
		if abs(team_one_points-team_two_points)<=3:
			outcome = "Tie"
		elif team_one_points>team_two_points:
			outcome = "Winner " + team_one_name
		else:
			outcome = "Winner " + team_two_name

		# draw results line
		self.add_widget(BorderedLabel(text="",size_hint=(self.sizes[0],None),height=ROW_HEIGHT))
		self.add_widget(BorderedLabel(text=team_one_name,size_hint=(self.sizes[1],None),height=ROW_HEIGHT))
		self.add_widget(BorderedLabel(text=str(team_one_points),size_hint=(self.sizes[2],None),height=ROW_HEIGHT))
		self.add_widget(BorderedLabel(text=outcome,size_hint=(self.sizes[3],None),height=ROW_HEIGHT))
		self.add_widget(BorderedLabel(text=team_two_name,size_hint=(self.sizes[4],None),height=ROW_HEIGHT))
		self.add_widget(BorderedLabel(text=str(team_two_points),size_hint=(self.sizes[5],None),height=ROW_HEIGHT))
		self.add_widget(BorderedLabel(text=str(jury_points),size_hint=(self.sizes[6],None),height=ROW_HEIGHT))
	

		# create data dictionary
		self.data = {}
		
		# team one data
		self.data["team_one_name"] = team_one_name
		self.data["team_one_points"] = team_one_points		
		self.data["team_one_point_diff"] = team_one_points - team_two_points

		# team two data
		self.data["team_two_name"] = team_two_name
		self.data["team_two_points"] = team_two_points		
		self.data["team_two_point_diff"] = team_two_points - team_one_points
	
		# assigning scores based on outcome
		if outcome == "Tie":
			self.data["team_one_score"] = 1
			self.data["team_two_score"] = 1

		elif team_one_points > team_two_points:
			self.data["team_one_score"] = 2
			self.data["team_two_score"] = 0

		else:
			self.data["team_one_score"] = 0
			self.data["team_two_score"] = 2

		# connect to database		
		cnx = create_connection()
		cnx.database = self.database_name
		cursor = cnx.cursor()


		# getting information about problems categories
		
		query = "select category from Problems_{} where day={} order by name;".format(self.category,self.round)
		cursor.execute(query)
		category_to_int = {"Alg.":0,"Comb.":1,"Geom.":2,"Num.":3}
		problem_categories = [category_to_int[result[0]] for result in cursor.fetchall()]

		# create for each person a list of scores 
		# ordering: Alg, Comb, Geom, Num Th, Total
		
		query = "select name from People_{} where team=\"{}\";".format(self.category,team_one_name)
		cursor.execute(query)
		self.data["team_one_people"] =  {result[0]:[0,0,0,0,0] for result in cursor.fetchall()}

		query = "select name from People_{} where team=\"{}\";".format(self.category,team_two_name)
		cursor.execute(query)
		self.data["team_two_people"] =  {result[0]:[0,0,0,0,0] for result in cursor.fetchall()}

		# go through each row and assign points to people
		for i in range(8):
			
			# check if there is information on this row else break
			if self.widgets[i][0].text=="": continue
			
			problem_number = int(self.widgets[i][0].text)-1
			problem_cat = problem_categories[problem_number]

			person_one_name = self.widgets[i][1].text
			person_one_score = int(self.widgets[i][2].text)

			person_two_name = self.widgets[i][4].text
			person_two_score = int(self.widgets[i][5].text)
			
			# assign scores to people
			self.data["team_one_people"][person_one_name][problem_cat]+=person_one_score
			self.data["team_one_people"][person_one_name][4] += person_one_score

			self.data["team_two_people"][person_two_name][problem_cat]+=person_two_score
			self.data["team_two_people"][person_two_name][4] += person_two_score

	def commit_data(self):
		
		# connect to database		
		cnx = create_connection()
		cnx.database = self.database_name
		cursor = cnx.cursor()

		# update Teams table
		t1s  = self.data["team_one_score"]
		t2s  = self.data["team_two_score"]

		t1p  = self.data["team_one_points"]
		t2p  = self.data["team_two_points"]		

		t1pd = self.data["team_one_point_diff"]
		t2pd = self.data["team_two_point_diff"]
	
		t1n  = self.data["team_one_name"]
		t2n  = self.data["team_two_name"]

		query1 = """update Teams_{} set rank_scores=rank_scores+{}, points=points+{},points_diff=points_diff+{} 
				where hidden_name=\"{}\"""".format(self.category,t1s,t1p,t1pd,t1n)

		query2 = """update Teams_{} set rank_scores=rank_scores+{}, points=points+{},points_diff=points_diff+{} 
				where hidden_name=\"{}\"""".format(self.category,t2s,t2p,t2pd,t2n)
		
		cursor.execute(query1)
		cursor.execute(query2)

		# update Matches table
		query = "update Matches_{} set protocol_set=1 where team_one=\"{}\" and team_two=\"{}\" and day={}".format(self.category,t1n,t2n,self.round)
		cursor.execute(query)

		# update People table
		for person in self.data["team_one_people"]:

			alg  = self.data["team_one_people"][person][0]
			comb = self.data["team_one_people"][person][1]
			geom = self.data["team_one_people"][person][2]
			num  = self.data["team_one_people"][person][3]
			tot  = self.data["team_one_people"][person][4]

			query = """update People_{} set alg_scores=alg_scores+{}, comb_scores=comb_scores+{}, geom_scores=geom_scores+{},
					num_scores=num_scores+{},total_scores=total_scores+{} where name=\"{}\" and team=\"{}\"""".format(self.category,alg,comb,geom,num,tot,person,t1n)
			cursor.execute(query)		

		
		for person in self.data["team_two_people"]:

			alg  = self.data["team_two_people"][person][0]
			comb = self.data["team_two_people"][person][1]
			geom = self.data["team_two_people"][person][2]
			num  = self.data["team_two_people"][person][3]
			tot  = self.data["team_two_people"][person][4]

			query = """update People_{} set alg_scores=alg_scores+{}, comb_scores=comb_scores+{}, geom_scores=geom_scores+{},
					num_scores=num_scores+{},total_scores=total_scores+{} where name=\"{}\" and team=\"{}\"""".format(self.category,alg,comb,geom,num,tot,person,t2n)
			cursor.execute(query)

		#f = open(,'w')


		# commit and close
		cnx.commit()
		cnx.close()
		
		
class NavigationButtons(GridLayout):

	def __init__(self,**kwargs):

		super(NavigationButtons,self).__init__(**kwargs)

		self.cols = 4

		self.padding = [0,20]
		self.spacing = 5

		self.add_widget(Button(text="Clear",size_hint_y = None, height=ROW_HEIGHT,on_press=(lambda x: self.clear())))
		self.add_widget(Button(text="Prev",size_hint_y = None,height=ROW_HEIGHT,on_press=(lambda x: self.go_prev())))
		self.add_widget(Button(text="Next",size_hint_y = None,height=ROW_HEIGHT,on_press=(lambda x: self.go_next())))
		self.add_widget(Button(text="Finish",size_hint_y = None,height=ROW_HEIGHT,on_press=(lambda x: self.finish())))
		

	def go_next(self):
		self.parent.go_next()

	def go_prev(self):
		self.parent.go_prev()

	def finish(self):
		self.parent.finish()

	def clear(self):
		self.parent.clear()


class DirectionRow(GridLayout):

	def __init__(self,row,**kwargs):

		super(DirectionRow,self).__init__(**kwargs)

		self.rows = 1

		self.add_widget(ToggleButton(font_name='myfont',font_size='22sp',text="→",group=str(row)))
		self.add_widget(ToggleButton(font_name='myfont',font_size='22sp',text="←",group=str(row)))
		self.add_widget(ToggleButton(font_name='myfont',font_size='22sp',text='⇆',group=str(row)))
		self.add_widget(ToggleButton(font_name='myfont',font_size='22sp',text='⇄',group=str(row)))

class MatchButtons(GridLayout):

	def __init__(self,**kwargs):

		super(MatchButtons,self).__init__(**kwargs)

		self.cols = 2

		self.padding = [150,20]
		self.spacing = 50

		self.add_widget(Button(text="Back",background_color = [1,0,0,1],on_press=(lambda x: self.close())))
		self.add_widget(Button(text="Continue",background_color = [0,0,1,1],on_press=(lambda x:self.commit())))

	def close(self):
		self.parent.close()

	def commit(self):
		self.parent.commit()


# enable bordering

class Bordered():
	pass


class BorderedLabel(Bordered,Label):
	pass

class ColoredLabel(Label):
	pass


