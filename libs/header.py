from qore import *
from . settings import Settings

class AppHeader(Widget):
	
	def __init__(self, terminal=None):
		super(self.__class__, self).__init__(terminal)
		self.terminal = terminal
		self.settings = Settings()
		
		self.data = {
			"system": self.settings.items['selected_system'],
			"client": self.settings.items['selected_client'],
			"user": self.settings.items['user']
		}

	def on_mount(self):
		self.set_interval(60, self.refresh)

	def render(self):
		grid = Table.grid(expand=True)
		grid.add_column(justify="left", ratio=1)
		grid.add_column(justify="left", ratio=1)
		grid.add_column(justify="right")

		if self.data != None:
			grid.add_row(
				"[b]Automic[/b] System Overview: {}:{}".format(self.data['system'].upper(), str(self.data['client'])),
				"[b]{}[/b]".format(self.data['user']),
				datetime.now().strftime("%d.%m.%Y %H:%M") #.replace(":", "[blink]:[/]"),
			)
		return Panel(grid, style="white on blue")