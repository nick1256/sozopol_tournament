import os

# kivy imports 
from kivy.app import App
from kivy.lang import Builder
from screens.python.screen_manager import MyScreenManager

# load all relevant kivy files
kivy_screens_path = "./screens/kivy/"
for filename in os.listdir(kivy_screens_path):
	Builder.load_file(kivy_screens_path+filename)

# create a screen manager
screen_manager = MyScreenManager()

# create the app
class SozopolApp(App):
	def build(self):
		return screen_manager


########## Execution ##########

if __name__=="__main__":
	app = SozopolApp()
	app.run()

