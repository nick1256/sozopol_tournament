#!/usr/bin/env python

"""
#######################################################################
# Info: Application for managing the Sozopol International Tournament #
# Written by: Nickolay Stoyanov										  #
# E-mail: nickolay.stoyanov.95@gmail.com							  #
# Last updated: 11/08/2017											  #
# Github repository: https://github.com/nick1256/sozopol_tournament   #
# Compatible with : Python 3										  #
#######################################################################
"""

# general imports
import os

# kivy imports
from kivy.app import App
from kivy.lang import Builder
from screens.python.screen_manager import MyScreenManager

# load all relevant kivy files
KIVY_PATH = "./screens/kivy/"
for filename in os.listdir(KIVY_PATH):
	Builder.load_file(KIVY_PATH+filename)

# create a screen manager
SCREEN_MANAGER = MyScreenManager()


class SozopolApp(App):
	"""Application class"""

	def build(self):
		return SCREEN_MANAGER


########## Execution ##########

if __name__ == "__main__":
	APP = SozopolApp()
	APP.run()
