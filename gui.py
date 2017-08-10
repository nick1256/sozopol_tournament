# screen imports
from screens.python.startscreen import StartScreen
from screens.python.createtournament import CreateTournamentScreen


# kivy imports 
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.core.window import Window

# load kivy files
Builder.load_file('./screens/kivy/start.kv')
Builder.load_file('./screens/kivy/createtournament.kv')


########## Screen Manager #########

#dict of all screen
screens = {}

# add start screen to screens
screens['start'] = StartScreen(name='start')

# add black screen to screen
screens['createtournament'] = CreateTournamentScreen(name="createtournament")


# create screen manager and all screens to it
sm = ScreenManager()

for screen_name in screens: 
	sm.add_widget(screens[screen_name]) 
	print(screen_name)

# start with start screen
go_to_window('start')



######### Sozopol App ##########

class SozopolApp(App):
	def build(self):
		return sm



########## Execution ##########

if __name__=="__main__":
	app = SozopolApp()
	app.run()
