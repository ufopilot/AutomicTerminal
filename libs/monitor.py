from qore import *
from . settings import Settings
from . automic import Automic

from  urllib.parse import quote
from datetime import datetime

class Monitor(Widget):
	def __init__(self, terminal=None, appheader=None):
		super(self.__class__, self).__init__(terminal)
		self.terminal = terminal
		self.title = "Monitoring"
		
		
	def on_mount(self):
		self.set_interval(15, self.refresh)
		
	def render(self):
		self.settings = Settings()
		self.system = self.settings.items['selected_system']
		self.client = self.settings.items['selected_client'] 
		if self.system == "" or self.client == "":
			return self.loading_panel(self.title)


		aut = Automic(self.system, self.client)
		aut.connect()
		data = aut.list_executions()
		
		if data == None:
			return Align.center(
		 		Panel("Error", title=self.title, height=100, expand=True, border_style="white"), 
		 		vertical="top", 
		 	)
		
		table = Table(padding=(0,1,0,1), show_header=True, show_lines=False, expand=True, border_style="bright_black", box=box.MINIMAL_DOUBLE_HEAD)
		table.add_column("Name", style="cyan", no_wrap=True)
		table.add_column("Runid", width=8, justify="left", style="magenta")
		table.add_column("Parentid", width=8, justify="left", style="magenta")
		table.add_column("User", width=8, style="green")
		table.add_column("Timestamp", width=16, style="white")
		table.add_column("Status", width=40)
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
		except:
			print("connect faild")
			exit()

		panel = Panel(
			table,
			padding=(0, 0),
			title="[b blue]Monitoring",
			border_style="blue",
			expand=True
		)
		return panel

	def loading_panel(self, title) -> Panel:
		panel = Panel(
			Align.center(
				Group("", "\n", Align.center("[bold red]No system selected")),
				vertical="top",
			),
			padding=(1, 2),
			title=f"[b bright_black]{title}",
			border_style="bright_black",
			height=100,
			expand=True
		)
		return panel