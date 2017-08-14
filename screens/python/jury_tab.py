# kivy imports
from kivy.uix.tabbedpanel import TabbedPanelItem
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.switch import Switch

# default row_height
ROW_HEIGHT = 40


# tab name with contents
class JuryTab(TabbedPanelItem):

	def __init__(self,screen,**kwargs):
		
		super(JuryTab,self).__init__(**kwargs)
		self.add_widget(JuryContents())


# contents
class JuryContents(GridLayout):
		
	def __init__(self,**kwargs):
		
		super(JuryContents,self).__init__(**kwargs)

		self.rows = 1
		self.cols = 3

		self.spacing = 20

		self.left_side  =  JuryButtons(self,size_hint_x = 0.1)		
		self.middle     =  JuryView(size_hint_x = 0.45)
		self.right_side =  JuryView(size_hint_x = 0.45)

		self.add_widget(self.left_side)
		self.add_widget(self.middle)
		self.add_widget(self.right_side)


	def add_jury(self):

		if self.middle.count < 20:		
			self.middle.add()
		else:
			self.right_side.add()

# buttons (left side)
class JuryButtons(GridLayout):
	
	def __init__(self,parent,**kwargs):

		super(JuryButtons,self).__init__(**kwargs)

		self.rows = 2
		self.cols = 1

		self.padding = [10,100]
		self.spacing = 10

		self.add_widget(Button(text="Add Jury",size_hint_y=None,height=ROW_HEIGHT,on_press=(lambda x: parent.add_jury())))
		self.add_widget(Button(text="Remove Jury",size_hint_y=None,height=ROW_HEIGHT))

# jury tables with headers (middle and right side)
class JuryView(GridLayout):
	
	def __init__(self,**kwargs):
		
		super(JuryView,self).__init__(**kwargs)
		
		
		self.rows = 2
		self.cols = 1	
		self.count = 0
	
		# Add Header 

		self.add_widget(JuryHeader(size_hint_y=0.1))
		self.jury_table = JuryTable(size_hint_y=0.9)
		self.add_widget(self.jury_table)


	def add(self):
		self.count+=1
		self.jury_table.add()

# headers
class JuryHeader(GridLayout):
	
	def __init__(self,**kwargs):

		super(JuryHeader,self).__init__(**kwargs)

		self.rows = 1
		self.cols = 6

		self.padding = 20	
	
		self.add_widget(BorderedLabel(text="Name",size_hint=(0.3,None),height=ROW_HEIGHT))
		self.add_widget(BorderedLabel(text="(6-7)",size_hint=(0.14,None),height=ROW_HEIGHT))
		self.add_widget(BorderedLabel(text="(8-9)",size_hint=(0.14,None),height=ROW_HEIGHT))
		self.add_widget(BorderedLabel(text="(10-12)",size_hint=(0.14,None),height=ROW_HEIGHT))
		self.add_widget(BorderedLabel(text="Alone",size_hint=(0.14,None),height=ROW_HEIGHT))
		self.add_widget(BorderedLabel(text="Active",size_hint=(0.14,None),height=ROW_HEIGHT))

# table
class JuryTable(GridLayout):
	
	def __init__(self,**kwargs):
		
		super(JuryTable,self).__init__(**kwargs)

		self.rows = 20
		self.cols = 1
		self.padding = 20


		self.count = 1

	def add(self):
		self.count+=1
		self.add_widget(JuryRow(self,size_hint_y=None,height=ROW_HEIGHT))
	
# rows of the table
class JuryRow(GridLayout):
	
	def __init__(self,parent,**kwargs):

		super(JuryRow,self).__init__(**kwargs)
	
		self.rows = 1
		self.cols = 6
	
		self.add_widget(BorderedLabel(text="Nickolay Stoyanov",size_hint=(0.3,None),height=ROW_HEIGHT))
		self.add_widget(BorderedSwitch(active=False,size_hint=(0.14,None),height=ROW_HEIGHT))
		self.add_widget(BorderedSwitch(active=False,size_hint=(0.14,None),height=ROW_HEIGHT))
		self.add_widget(BorderedSwitch(active=False,size_hint=(0.14,None),height=ROW_HEIGHT))
		self.add_widget(BorderedSwitch(active=False,size_hint=(0.14,None),height=ROW_HEIGHT))
		self.add_widget(BorderedSwitch(active=False,size_hint=(0.14,None),height=ROW_HEIGHT))		

# borderding
class Bordered():
	pass

class BorderedLabel(Bordered,Label):
	pass

class BorderedSwitch(Bordered,Switch):
	pass

class BorderedTextInput(Bordered,TextInput):
	pass
