from qore import *
from libs.menu import Menu
from libs.monitor import Monitor
from libs.agents import Agents
from libs.header import AppHeader
from libs.health import Health

class AutomicTerminal(App):
	async def on_load(self) -> None:
		"""Bind keys here."""
		await self.bind("a", "toggle_assembly", "Toggle Assembly")
		await self.bind("r", "toggle_report", "Toggle Report Viewer")
		await self.bind("q", "quit", "Quit")
		#await self.bind("m", "quit", "Monitor")

	show_assembly = Reactive(False)
	show_report = Reactive(False)

	def watch_show_assembly(self, show_assembly: bool) -> None:
		"""Called when show_assembly changes."""
		self.assembly.animate("layout_offset_x", 0 if show_assembly else -40, duration=0.5)
		self.explorer.animate("layout_offset_x", 0 if show_assembly else -240, duration=0.5)
	
	def watch_show_report(self, show_report: bool) -> None:
		"""Called when show_report changes."""
		self.report.animate("layout_offset_x", 0 if show_report else -40, duration=0.5)

	def action_toggle_assembly(self) -> None:
		"""Called when user hits toggle key."""
		self.show_assembly = not self.show_assembly
	
	def action_toggle_report(self) -> None:
		"""Called when user hits toggle key."""
		self.show_report = not self.show_report

	async def on_mount(self) -> None:

		"""Build layout here."""
		self.footer = Footer()
		self.header = header = ScrollView(auto_width=False)
		self.right = right = Menu()
		self.right.terminal = self
		
		self.left = left = ScrollView(auto_width=False)
		self.main = main = ScrollView(auto_width=False)
		
		self.sub_header = Widget(name="sub_header")
		self.top_header = top_header = ScrollView(auto_width=False) 
		#= Widget(name="top_header")
		self.bottom = Widget(name="bottom")

		self.assembly = Widget(name="assembly")
		self.explorer = Widget(name="explorer")
		self.report = Widget(name="report")
		
		# docks
		await self.view.dock(self.header, edge="top", size=3)
		await self.view.dock(self.footer, edge="bottom")
	   
		await self.view.dock(self.bottom, edge="bottom", size=5)
		 
		await self.view.dock(self.left, edge="left", size=30)
		await self.view.dock(self.top_header, self.sub_header, edge="top", size=5)
		await self.view.dock(self.right, edge="right", size=17)
		await self.view.dock(self.main, edge="right")
		await self.view.dock(self.assembly, edge="left", size=40, z=1)
		await self.view.dock(self.explorer, edge="left", size=200, z=1)
		await self.view.dock(self.report, edge="left", size=40, z=2)
		
		self.assembly.layout_offset_x = -40
		self.explorer.layout_offset_x = -240
		self.report.layout_offset_x = -40
		#self.right.layout_offset_x = +400
		
		async def add_content():
			
			#### init Header
			appheader = AppHeader()
			agents = Agents()
			monitor = Monitor()
			health = Health()

			right.appheader = appheader
			right.health = health  
			right.agents = agents
			right.monitor = monitor
			
			await header.update(appheader)
			await left.update(agents)
			await main.update(monitor)
			await top_header.update(health)
			
			#init Monitor Panel
			#await main.update(Monitor())
			
			#init Agents Panel
			#await left.update(Agents())
			
			#init Menu Panel
			#######await right.update(Menu())
			########
			
		await self.call_later(add_content)

AutomicTerminal.run(title="Automic", log="textual.log")
