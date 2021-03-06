from qore import *
from . settings import Settings
from . automic import Automic

from  urllib.parse import quote
from datetime import datetime

class Agents(Widget):
	def __init__(self, terminal=None, appheader=None):
		super(self.__class__, self).__init__(terminal)
		self.terminal = terminal
		self.settings = Settings()
		self.panel = "agents"
		self.title = self.settings.items['panels'][self.panel]['title']
		self.border_style = self.settings.items['panels'][self.panel]['border_style']
		self.refresh_time = self.settings.items['panels'][self.panel]['refresh_time']
		self.max_rows = self.settings.items['panels']['monitor']['max_rows']
		
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

		data = aut.list_agents()
		
		if data == None:
			return self.error_panel("Rest-request error")
		
		#table = Table(padding=(0,1,0,1), show_header=True, show_lines=False, expand=True, border_style="bright_black", box=box.MINIMAL_DOUBLE_HEAD)
		table = Table(expand=False, border_style="bright_black", box=box.MINIMAL_DOUBLE_HEAD)
		table.add_column("Name", style="cyan", no_wrap=True, width=30)
		table.add_column("Status", width=15)
		
		try:	
			for o in data:
				if o['active']:
					status = "[b green]On"
				else:
					status = "[b red]Off"
				table.add_row( o['name'], status)
			
			for x in range(self.max_rows):
				table.add_row("", "")		
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