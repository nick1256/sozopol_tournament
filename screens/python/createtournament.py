from kivy.uix.screenmanager import Screen

########## Create Tournament Screen ########## 

class CreateTournamentScreen(Screen):
	
	def __init__(self,name,screen_manager):
		
		super(CreateTournamentScreen,self).__init__()
		self.name = name
		self.window_size = (300,400)
		self.screen_manager = screen_manager


	def get_info(self,teams,days,name):
		
		# convert to int and adjust for defaults
		teams = int(teams)
		if days=="" : days = 5
		else: days = int(days)

		if name=="" : name="Sozopol_2017"
			
		print(num_of_teams,num_of_days,tournament_name)

