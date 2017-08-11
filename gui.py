# screen imports
from screens.python.start import StartScreen
from screens.python.createtournament import CreateTournamentScreen
from screens.python.screen_manager import MyScreenManager

# kivy imports 
from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window

# load kivy files
Builder.load_file('./screens/kivy/start.kv')
Builder.load_file('./screens/kivy/createtournament.kv')


########## Screen Manager #########

# init
screen_manager = MyScreenManager()

# start screen
start = StartScreen('start',screen_manager)

# create tournament screen
create_tournament = CreateTournamentScreen("createtournament",screen_manager)

# screen manager
screen_manager.add(start)
screen_manager.add(create_tournament)
screen_manager.set('start')


######### Sozopol App ##########

class SozopolApp(App):
	def build(self):
		return screen_manager



########## Execution ##########

if __name__=="__main__":
	app = SozopolApp()
	app.run()
