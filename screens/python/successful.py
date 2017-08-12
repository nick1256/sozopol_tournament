#kivy imports
from kivy.uix.screenmanager import Screen

# mysql imports
import mysql.connector as mysqlc
from mysql.connector import errorcode

# file imports
from utilities.create_connection import create_connection

# Abstract Successful Class
class SuccessfulScreen(Screen):
	
	def __init__(self,name,screen_manager):

		self.name = name
		self.screen_manager = screen_manager
		self.window_size = (500,400)
		

		### information string and relevant info

		# connect database
		cnx = create_connection()
		cnx.database = self.screen_manager.database_name
		cursor = cnx.cursor()

		# get information from database
		cursor.execute("select value from Variables where name=\"tournament_name\";")
		tname = cursor.fetchall()[0][0]
	
		cursor.execute("select value from Variables where name=\"number_rounds\";")
		nrounds = cursor.fetchall()[0][0]

		cursor.execute("select value from Variables where name=\"number_teams_small\";")
		nsmall = cursor.fetchall()[0][0]

		cursor.execute("select value from Variables where name=\"number_teams_medium\";")
		nmedium = cursor.fetchall()[0][0]

		cursor.execute("select value from Variables where name=\"number_teams_big\";")
		nbig = cursor.fetchall()[0][0]

		self.information_string = """Name of Tournament: {} \n
									 Number of Rounds: {} \n
							   		 Number of Teams (6-7): {} \n
				    				 Number of Teams (8-9): {} \n
				    			 	 Number of Teams (10-12): {} """.format(tname,nrounds,nsmall,nmedium,nbig)
			
			

		super(SuccessfulScreen,self).__init__()


# Concrete Classes
class SuccessfulCreateScreen(SuccessfulScreen):
	
	def __init__(self,name,screen_manager):
		
		self.back_screen_name = "create_continued_big"
		self.upper_label_text = "Created Tournament successfully!"	
		super(SuccessfulCreateScreen,self).__init__(name,screen_manager)
			

class SuccessfulLoadScreen(SuccessfulScreen):
	
	def __init__(self,name,screen_manager):
		
		self.back_screen_name = "start"
		self.upper_label_text = "Loaded Tournament successfully!"
		super(SuccessfulLoadScreen,self).__init__(name,screen_manager)
	
