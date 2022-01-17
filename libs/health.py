from qore import *
from . settings import Settings
from . automic import Automic

class Health(Widget):
	def __init__(self, terminal=None):
		super(self.__class__, self).__init__(terminal)
		self.terminal = terminal
		self.settings = Settings()
		self.panel = "health"
		self.title = self.settings.items['panels'][self.panel]['title']
		self.border_style = self.settings.items['panels'][self.panel]['border_style']
		self.refresh_time = self.settings.items['panels'][self.panel]['refresh_time']
		
		
	def on_mount(self):
		self.set_interval(self.refresh_time, self.refresh)
		
	def render(self):
		
		self.settings = Settings()
		self.system = self.settings.items['selected_system']
		self.client = self.settings.items['selected_client'] 
		if self.system == "" or self.client == "":
			return self.error_panel("No system selected")

		aut = Automic(self.system, self.client)
		if not aut.connect():
			return self.error_panel("Connection error")

		data = aut.health_check()
		
		if data == None:
			return self.error_panel("Rest-request error")
		
		table = Table(expand=True, border_style="bright_black", box=box.MINIMAL_DOUBLE_HEAD, show_header=False, style="cyan")
		table.add_column("GLOBAL", style="cyan", no_wrap=True, justify="center")
		table.add_column("PWP", style="cyan", no_wrap=True, justify="center")
		table.add_column("JWP", style="cyan", no_wrap=True, justify="center")
		table.add_column("CP", style="cyan", no_wrap=True, justify="center")
		
		try:
			if data['status'] == "UP":
				global_color = "green"
			else:
				global_color = "red"

			if data['pwp']['status'] == "UP":
				pwp_color = "green"
			else:
				pwp_color = "red"
			
			if data['jwp']['status'] == "UP":
				jwp_color = "green"
			else:
				jwp_color = "red"

			if data['cp']['status'] == "UP":
				cp_color = "green"
			else:
				cp_color = "red"

			table.add_row(
				f"Global Status:[{global_color}]{data['status']}",
				f"PWP: Status:[{pwp_color}]{data['pwp']['status']}, [cyan]Instances:[yellow]{data['pwp']['instancesRunning']}",
				f"JWP: Status:[{jwp_color}]{data['jwp']['status']}, [cyan]Instances:[yellow]{data['jwp']['instancesRunning']}",
				f"CP: Status:[{cp_color}]{data['cp']['status']}, [cyan]Instances:[yellow]{data['cp']['instancesRunning']}"
			)

		except:
			return self.error_panel("Can't read response data properly.")

		panel = Panel(
			table,
			padding=(0, 0),
			title=f"[b blue]{self.title}",
			border_style=f"{self.border_style}",
			expand=True
		)
		return panel

	def error_panel(self, message):
		return Panel(
				f"[b red]{message}",
				padding=(0, 0),
				title=f"[b blue]{self.title}",
				border_style="bright_black"
			)