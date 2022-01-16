from email import header
from qore import *

class Menu(GridView):
	# #Header = parent
	# DARK = "white on rgb(51,51,51)"
	# LIGHT = "black on rgb(165,165,165)"
	# YELLOW = "white on rgb(255,159,7)"

	# BUTTON_STYLES = {
	#     "AC": LIGHT,
	#     "C": LIGHT,
	#     "+/-": LIGHT,
	#     "%": LIGHT,
	#     "/": YELLOW,
	#     "X": YELLOW,
	#     "-": YELLOW,
	#     "+": YELLOW,
	#     "=": YELLOW,
	# }

	# def __init__(self, parent=None, *args, **kwargs):
	#    #super(Menu, self).__init__(*args, **kwargs)
	#    super().__init__(args, parent)
	#    self.parent = parent
	
	def __init__(self, terminal=None):
		super(self.__class__, self).__init__(terminal)
		self.terminal = terminal
	
	def on_mount(self) -> None:
		def make_button(text: str, style: str) -> Button:
			"""Create a button with the given Figlet label."""
			return Button(text, style=style, name=text)

		# Make all the buttons
		self.buttons = {
			name: make_button(name, "black on rgb(165,165,165)")
			for name in "PRODZPL1,PRODZPL2,PRODZPL3,PRODZPL4,PRODZPL5,PRODZPL6, PRODZPL7, PRODZPL8, PRODZPL9, PRODZPL10, PRODZPL11, PRODZPL12, PRODZPL13, PRODZPL14".split(",")
		}

		# Buttons that have to be treated specially
		# Set basic grid settings
		self.grid.set_gap(1, 1)
		self.grid.set_gutter(1)
		self.grid.set_align("left", "center")
		# # Create rows / columns / areas
		self.grid.add_column("col1", max_size=20)
		#self.grid.add_row("numbers", max_size=15)
		self.grid.add_row("system", max_size=10, repeat=14)
		self.grid.add_areas(
			system="col1-start|col1-end,system"
		)
		# Place out widgets in to the layout
		#self.grid.place(clear=self.c)
		self.grid.place(
			*self.buttons.values()
		)

	async def handle_button_pressed(self, message: ButtonPressed) -> None:
		"""A message sent by the button widget"""

		assert isinstance(message.sender, Button)
		button_name = message.sender.name

		await self.terminal.main.update(Panel(button_name.strip()))
		
		
		def do_math() -> None:
			"""Does the math: LEFT OPERATOR RIGHT"""
			self.log(self.left, self.operator, self.right)
			try:
				if self.operator == "+":
					self.left += self.right
				elif self.operator == "-":
					self.left -= self.right
				elif self.operator == "/":
					self.left /= self.right
				elif self.operator == "X":
					self.left *= self.right
				self.display = str(self.left)
				self.value = ""
				self.log("=", self.left)
			except Exception:
				self.display = "Error"


		# if button_name.isdigit():
		# 	self.display = self.value = self.value.lstrip("0") + button_name
		# elif button_name == "+/-":
		# 	self.display = self.value = str(Decimal(self.value or "0") * -1)
		# elif button_name == "%":
		# 	self.display = self.value = str(Decimal(self.value or "0") / Decimal(100))
		# elif button_name == ".":
		# 	if "." not in self.value:
		# 		self.display = self.value = (self.value or "0") + "."
		# elif button_name == "AC":
		# 	self.value = ""
		# 	self.left = self.right = Decimal(0)
		# 	self.operator = "+"
		# 	self.display = "0"
		# elif button_name == "C":
		# 	self.value = ""
		# 	self.display = "0"
		# elif button_name in ("+", "-", "/", "X"):
		# 	self.right = Decimal(self.value or "0")
		# 	do_math()
		# 	self.operator = button_name
		# elif button_name == "=":
		# 	if self.value:
		# 		self.right = Decimal(self.value)
		# 	do_math()


# class CalculatorApp(App):
#     """The Calculator Application"""

#     async def on_mount(self) -> None:
#         """Mount the calculator widget."""
#         await self.view.dock(Calculator())


# CalculatorApp.run(title="Calculator Test", log="textual.log")
