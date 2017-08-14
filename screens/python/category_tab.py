# kivy imports
from kivy.uix.tabbedpanel import TabbedPanelItem
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label

# mysql imports
import mysql.connector as mysqlc
from mysql.connector import errorcode

# file imports
from utilities.create_connection import create_connection


class CategoryTab(TabbedPanelItem):

	def __init__(self,screen,category,**kwargs):
		
		super(CategoryTab,self).__init__(**kwargs)
		self.add_widget(CategoryContents(screen,category))
		

class CategoryContents(GridLayout):
	
	def __init__(self,screen,category,**kwargs):
	
		super(CategoryContents,self).__init__(**kwargs)
		
		self.rows = 1
		self.cols = 3

		left= Label(text="Buttons",size_hint_x = 0.15)

		middle = CategoryTable(screen,category,size_hint_x=0.6)

		right = Label(text="Round",size_hint_x = 0.25)

		self.add_widget(left)
		self.add_widget(middle)
		self.add_widget(right)

class CategoryTable(GridLayout):
		
	def __init__(self,screen,category,**kwargs):

		super(CategoryTable,self).__init__(**kwargs)

		# get relevant information for number of teams from mysql

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

class Bordered():
	pass

class BorderedLabel(Bordered,Label):
	pass

