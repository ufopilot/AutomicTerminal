from qore import *
from . settings import Settings
from . automic import Automic

from  urllib.parse import quote
from datetime import datetime

class Monitor(Widget):
	def __init__(self, terminal=None, appheader=None):
		super(self.__class__, self).__init__(terminal)
		self.terminal = terminal
		self.settings = Settings()
		self.title = self.settings.items['panels']['monitor']['title']
		self.border_style = self.settings.items['panels']['monitor']['border_style']
		self.refresh_time = self.settings.items['panels']['monitor']['refresh_time']
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
		aut.connect()
		aut = Automic(self.system, self.client)
		
		if not aut.connect():
			return self.error_panel("Connection error")

		data = aut.list_executions()
		if data == None:
			return self.error_panel("Rest-request error")
		
		
		table = Table(padding=(0,1,0,1), show_header=True, show_lines=False, expand=True, border_style="bright_black", box=box.MINIMAL_DOUBLE_HEAD)
		table.add_column("Name", style="cyan", no_wrap=True)
		table.add_column("Runid", width=9, justify="left", style="magenta")
		table.add_column("Parentid", width=9, justify="left", style="magenta")
		table.add_column("User", width=8, style="green")
		table.add_column("Timestamp", width=19, style="white")
		table.add_column("Status", width=50)
		awiurl = self.settings.items['systems'][self.system]['awi_url']    
		#table.add_row("Raising shields", "[bold magenta]COMPLETED [green]:heavy_check_mark:")        
		try: 
			
			for o in data:
				repurl = "{}:{}@pm/report/{}&runid={}&src=eh&type={}".format(str(self.system).upper(), str(self.client), o['name'], str(o['run_id']), o['type'])    
				repurl = quote(repurl, safe='')
				repurl = f"{awiurl}#{repurl}"
				
				if o['status'] <= 1600:
					color = "green"
				elif o['status'] >= 1600 and o['status'] <= 1799:
					color = "blue"
				elif o['status'] >= 1800 and o['status'] <= 1899:
					color = "red"
				else:
					color = "white"

				if "start_time" in o:
					time = o['start_time']
				else:
					time = o['activation_time']
				status_text = (o['status_text'][:40] + '..') if len(o['status_text']) > 40 else o['status_text']
				
				table.add_row(
					o['name'],
					f"[u cyan link={repurl}]{str(o['run_id'])}",
					str(o['parent']),
					o['user'],
					str(time.replace('T', ' ').replace('Z', '').replace(" ","_")),
					f"[{color}]{status_text}"
				)

			for x in range(self.max_rows):
				table.add_row("", "","", "","", "")
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