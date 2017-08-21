# kivy imports 
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton

class ProblemsPopup(GridLayout):
	
	def __init__(self,popup,**kwargs):

		super(ProblemsPopup,self).__init__(**kwargs)
		self.popup = popup

		self.rows = 9
		self.cols = 1

		self.spacing = 10
		self.padding = 10

		# add the 8 problems rows

		for problem_num in range(8):
			self.add_widget(ProblemsRow(str(problem_num+1)))

		# add buttons
		self.add_widget(ProblemsButtons())


	def dismiss(self):
		self.popup.dismiss()


class ProblemsRow(GridLayout):
	
	def __init__(self,number,**kwargs):
		
		super(ProblemsRow,self).__init__(**kwargs)

		self.rows = 1
		self.cols = 5

		self.spacing = 10
		self.padding = 10

		self.add_widget(Label(text="Problem {}:".format(number)))

		self.add_widget(ToggleButton(text="Alg.",group=number))
		self.add_widget(ToggleButton(text="Comb.",group=number))
		self.add_widget(ToggleButton(text="Geom.",group=number))
		self.add_widget(ToggleButton(text="Num.",group=number))


class ProblemsButtons(GridLayout):

	def __init__(self,**kwargs):
		
		super(ProblemsButtons,self).__init__(**kwargs)

		self.rows = 1
		self.cols = 2

		self.spacing = 100
		self.padding = [50,10]

		self.add_widget(Button(text="Back",background_color = [1,0,0,1],on_press=(lambda x: self.parent.dismiss())))
		self.add_widget(Button(text="Continue",background_color = [0,0,1,1],on_press=(lambda x: self.parent.dismiss())))
		




