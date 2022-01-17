from qore import *
from libs.menu import Menu
from libs.monitor import Monitor
from libs.agents import Agents
from libs.header import AppHeader

class AutomicTerminal(App):
	async def on_load(self) -> None:
		"""Bind keys here."""
		await self.bind("t", "toggle_sidebar", "Toggle Menu")
		await self.bind("q", "quit", "Quit")
		#await self.bind("m", "quit", "Monitor")

	show_bar = Reactive(False)

	def watch_show_bar(self, show_bar: bool) -> None:
		"""Called when show_bar changes."""
		self.sidebar.animate("layout_offset_x", 0 if show_bar else -40)

	def action_toggle_sidebar(self) -> None:
		"""Called when user hits toggle key."""
		self.show_bar = not self.show_bar

	async def on_mount(self) -> None:

		"""Build layout here."""
		self.footer = Footer()
		self.header = header = ScrollView(auto_width=False)
		self.right = right = Menu()
		self.right.terminal = self
		
		self.left = left = ScrollView(auto_width=False)
		self.main = main = ScrollView(auto_width=True)
		
		self.sub_header = Placeholder(name="sub_header")
		self.top_header = Placeholder(name="top_header")
		self.bottom = Placeholder(name="bottom")

		self.sidebar = Widget(name="blub")
		
		# docks
		await self.view.dock(self.header, edge="top", size=3)
		await self.view.dock(self.footer, edge="bottom")
	   
		await self.view.dock(self.bottom, edge="bottom", size=5)
		 
		await self.view.dock(self.left, edge="left", size=30)
		await self.view.dock(self.top_header, self.sub_header, edge="top", size=5)
		await self.view.dock(self.right, edge="right", size=20)
		await self.view.dock(self.main, edge="right")
		await self.view.dock(self.sidebar, edge="left", size=40, z=1)
		
		self.sidebar.layout_offset_x = -40

		async def add_content():
			
			#### init Header
			appheader = AppHeader()
			right.appheader = appheader
			await header.update(appheader)
			
			#init Monitor Panel
			await main.update(Monitor())
			
			#init Agents Panel
			await left.update(Agents())
			
			#init Menu Panel
			#######await right.update(Menu())
			########
			
		await self.call_later(add_content)


AutomicTerminal.run(title="Automic", log="textual.log")
