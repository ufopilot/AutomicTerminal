from qore import *
class Agents(Widget):
    def on_mount(self):
        self.set_interval(113, self.refresh)
        

    def render(self):
        self.title = "Agents"
        table = Table(expand=True)
        for i in range(2):
            table.add_column(f"Col {i + 1}", style="magenta")
        for i in range(random.randint(1,9)):
            table.add_row(*[f"cell {i},{j}" for j in range(2)])
        
        return Align.center(
            Panel(table, title=self.title, width=40, height=1000, border_style="white"), 
            vertical="top", 
        )