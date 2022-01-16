from qore import *
class Monitor(Widget):
    def on_mount(self):
        self.set_interval(3, self.refresh)
        self.s = 0
        self.title = "Monitoring"

    def render(self):
        #view = ScrollView(auto_width=True)
        self.title = "Monitoring"
        table = Table(expand=True)
        for i in range(3):
            table.add_column(f"Col {i + 1}", style="magenta")
        for i in range(random.randint(1,100)):
            table.add_row(*[f"cell {i},{j}" for j in range(3)])
        
        #view.upadte(table)
        #return table

        # self.table = Table(expand=True, show_header=False, show_lines=False, padding=(0,0,1,1), border_style="black")
        # self.menu.add_column()
        # for system in ("PRODADM1", "INTEALL1", "PRODZPL1", "PRODZPL2", str(random.randint(1,40))):
        #     self.menu.add_row(Button(system, style=self.LIGHT, name=system))

        return Align.center(
            Panel(table, title=self.title, width=150, border_style="white", expand=True), 
            vertical="top", 
        )