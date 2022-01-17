from qore import *
from . settings import Settings

class Menu(GridView):
	DARK = "white on rgb(51,51,51)"
	LIGHT = "black on rgb(165,165,165)"
	YELLOW = "black on rgb(255,159,7)"

	def __init__(self, terminal=None, appheader=None):
		super(self.__class__, self).__init__(terminal)
		self.terminal = terminal
		self.appheader = appheader
		self.settings = Settings()

	def on_mount(self) -> None:

		
		#self.body = body = ScrollView(auto_width=True)
		#self.view.dock(body)

		def make_button(text: str, style: str) -> Button:
			"""Create a button with the given Figlet label."""
			return Button(text, style=style, name=text)

		# Make all the buttons
		counter = 1
		list = []
		for name in self.settings.items['systems'].keys():
			for client in  self.settings.items['systems'][name]['clients']:
				list.append(f"{name.upper()}_{str(client).zfill(4)}")
				counter += 1

		self.buttons = {
			name: make_button(name, self.YELLOW)
			for name in list
		}

		# Buttons that have to be treated specially
		# Set basic grid settings
		self.grid.set_gap(1, 1)
		self.grid.set_gutter(1)
		self.grid.set_align("left", "center")
		# # Create rows / columns / areas
		self.grid.add_column("col1", max_size=20)
		self.grid.add_row("system", max_size=10, repeat=14)
		self.grid.add_areas(
			system="col1-start|col1-end,system"
		)
		# Place out widgets in to the layout
		self.grid.place(
			*self.buttons.values()
		)

		#body.update(self.grid)

	def handle_button_pressed(self, message: ButtonPressed) -> None:
		"""A message sent by the button widget"""

		assert isinstance(message.sender, Button)
		button_name = message.sender.name

		self.appheader.data['system'] = button_name.strip().split('_')[0]
		self.appheader.data['client'] = button_name.strip().split('_')[1]
		self.settings.items['selected_system'] = button_name.strip().split('_')[0].lower()
		self.settings.items['selected_client'] = button_name.strip().split('_')[1]
		self.settings.serialize()
		