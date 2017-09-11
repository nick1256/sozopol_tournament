""" Jury Tab """
# kivy imports
from kivy.uix.tabbedpanel import TabbedPanelItem
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.switch import Switch

# file imports
# pylint: disable=E0401
from utilities.create_connection import create_connection
from utilities.inserters import insert_jury_member

# default row_height
ROW_HEIGHT = 35


class JuryTab(TabbedPanelItem):
	""" tab name with contents """

	def __init__(self, database_name, **kwargs):

		super(JuryTab, self).__init__(**kwargs)
		self.add_widget(JuryView(database_name))


class JuryView(GridLayout):
	""" contents """

	def __init__(self, database_name, **kwargs):

		super(JuryView, self).__init__(**kwargs)

		self.rows = 1
		self.cols = 4

		self.spacing = 20

		self.left_side = JuryButtons(self, size_hint_x=0.1)
		self.middle = JuryContents(size_hint_x=0.45)
		self.right_side = JuryContents(size_hint_x=0.45)

		self.add_widget(self.left_side)
		self.add_widget(self.middle)
		self.add_widget(self.right_side)

		# get database name and load jury
		self.database_name = database_name
		self.load_jury()

	def add_jury(self):
		""" add jury member """

		if self.middle.count < 25:
			self.middle.add()
		else:
			self.right_side.add()

	def remove_jury(self):
		""" remove jury member """

		if self.right_side.count > 0:
			self.right_side.remove()

		elif self.middle.count > 0:
			self.middle.remove()

	def load_jury(self):
		""" load previous data """

		# connect to database
		cnx = create_connection()
		cnx.database = self.database_name
		cursor = cnx.cursor()

		# get information
		cursor.execute("select * from Jury order by active desc, small desc, medium desc, big desc, alone desc, name;")

		for jury_member in cursor.fetchall():

			name = jury_member[0]
			states = jury_member[1:]

			if self.middle.count < 25:
				self.middle.load({'name':name, 'states':states})
			else:
				self.right_side.load({'name':name, 'states':states})

	def save_jury(self):
		""" save data """

		values1 = self.middle.save()
		values2 = self.right_side.save()

		# connect to database
		cnx = create_connection()
		cnx.database = self.database_name
		cursor = cnx.cursor()

		# clear Jury Table
		cursor.execute("truncate Jury;")

		# add members with renewed information
		for jury_member in values1:
			if jury_member[0] == "":
				continue

			insert_jury_member(cursor, jury_member)

		for jury_member in values2:
			if jury_member[0] == "":
				continue

			insert_jury_member(cursor, jury_member)

		# commit data
		cnx.commit()

		# sort data
		self.middle.clear()
		self.right_side.clear()
		self.load_jury()

class JuryButtons(GridLayout):
	""" buttons (left side) """

	def __init__(self, parent, **kwargs):

		super(JuryButtons, self).__init__(**kwargs)

		self.rows = 3
		self.cols = 1

		self.padding = [10, 100]
		self.spacing = 10

		self.add_widget(Button(text="Add Jury", size_hint_y=None, height=ROW_HEIGHT, on_press=(lambda x: parent.add_jury())))
		self.add_widget(Button(text="Remove Jury", size_hint_y=None, height=ROW_HEIGHT, on_press=(lambda x: parent.remove_jury())))
		self.add_widget(Button(text="Save Changes", size_hint_y=None, height=ROW_HEIGHT, on_press=(lambda x: parent.save_jury())))

class JuryContents(GridLayout):
	""" jury tables with headers (middle and right side) """

	def __init__(self, **kwargs):

		super(JuryContents, self).__init__(**kwargs)

		self.rows = 2
		self.cols = 1
		self.count = 0

		# Add Header
		self.add_widget(JuryHeader(size_hint_y=0.1))
		self.jury_table = JuryTable(size_hint_y=0.9)
		self.add_widget(self.jury_table)


	def add(self):
		""" add member """
		self.count += 1
		self.jury_table.add()

	def remove(self):
		""" remove member """
		self.count -= 1
		self.jury_table.remove()

	def load(self, args):
		""" load """
		self.count += 1
		self.jury_table.load(args)

	def clear(self):
		""" clear """
		self.count = 0
		self.jury_table.clear()

	def save(self):
		""" save """
		return self.jury_table.save()


class JuryHeader(GridLayout):
	""" headers """

	def __init__(self, **kwargs):

		super(JuryHeader, self).__init__(**kwargs)

		self.rows = 1
		self.cols = 6

		self.padding = 20

		self.add_widget(BorderedLabel(text="Name", size_hint=(0.3, None), height=ROW_HEIGHT))
		self.add_widget(BorderedLabel(text="(6-7)", size_hint=(0.14, None), height=ROW_HEIGHT))
		self.add_widget(BorderedLabel(text="(8-9)", size_hint=(0.14, None), height=ROW_HEIGHT))
		self.add_widget(BorderedLabel(text="(10-12)", size_hint=(0.14, None), height=ROW_HEIGHT))
		self.add_widget(BorderedLabel(text="Alone", size_hint=(0.14, None), height=ROW_HEIGHT))
		self.add_widget(BorderedLabel(text="Active", size_hint=(0.14, None), height=ROW_HEIGHT))


class JuryTable(GridLayout):
	""" table with jury members """

	def __init__(self, **kwargs):

		super(JuryTable, self).__init__(**kwargs)

		self.rows = 25
		self.cols = 1
		self.padding = 20

		self.count = 0
		self.widgets = []

	def add(self):
		""" add a row """

		self.widgets.append(JuryRow(self, size_hint_y=None, height=ROW_HEIGHT))
		self.add_widget(self.widgets[-1])
		self.count += 1

	def remove(self):
		""" remove a row """

		last_widget = self.widgets[-1]
		self.clear_widgets([last_widget])
		self.widgets.pop()

	def load(self, args):
		""" load rows """

		self.widgets.append(JuryRow(self, loaded=True, loaded_args=args, size_hint_y=None, height=ROW_HEIGHT))
		self.add_widget(self.widgets[-1])
		self.count += 1

	def save(self):
		""" save data """
		return [child.save() for child in self.children]

	def clear(self):
		""" clear data """
		self.count = 0
		self.clear_widgets(self.children)


class JuryRow(GridLayout):
	"""	row of the table """

	def __init__(self, parent, loaded=False, loaded_args=None, **kwargs):

		super(JuryRow, self).__init__(**kwargs)

		self.rows = 1
		self.cols = 6
		self.parent_widget = parent
		self.widgets = []

		if not loaded:
			self.create_new()
		else:
			self.create_loaded(loaded_args)


	def create_new(self):
		""" create NEW row """

		# textinput for name
		self.widgets.append(TextInput(size_hint=(0.3, None), multiline=False, height=ROW_HEIGHT, on_text_validate=lambda x: self.change()))

		# add first three switches defaulting to values in switches
		switches = [0, 0, 0, 1, 1]
		for i in range(5):
			self.widgets.append(BorderedSwitch(active=switches[i], disabled=True, size_hint=(0.14, None), height=ROW_HEIGHT))

		# add widges to screen
		for widget in self.widgets:
			self.add_widget(widget)

	def change(self):
		""" change from textinput to label """

		# delete widgets
		self.clear_widgets(self.widgets)

		# change first one to label from textinput
		self.widgets[0] = BorderedLabel(text=self.widgets[0].text, size_hint=(0.3, None), height=ROW_HEIGHT)
		self.add_widget(self.widgets[0])

		# redraw
		for widget in self.widgets[1:]:
			widget.disabled = False
			self.add_widget(widget)

	def save(self):
		""" save data """

		values = [self.widgets[0].text]
		for i in range(1, 6):
			values.append(1 if self.widgets[i].active else 0)

		return values

	def create_loaded(self, args):
		""" create a row from loaded data """

		# create label
		self.widgets.append(BorderedLabel(text=args['name'], size_hint=(0.3, None), height=ROW_HEIGHT))

		# create states
		for i in range(5):
			self.widgets.append(BorderedSwitch(active=args['states'][i], size_hint=(0.14, None), height=ROW_HEIGHT))

		# draw
		for widget in self.widgets:
			self.add_widget(widget)

# borderding
class Bordered():
	""" bordering"""
	pass

class BorderedLabel(Bordered, Label):
	""" bordered label """
	pass

class BorderedSwitch(Bordered, Switch):
	""" bordered switch """
	pass
