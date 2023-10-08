import tkinter as tk
from app.views.main_view import MainView
from app.controllers.main_controller import MainController
from app.models.model import WebDataModel


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("FilePursuit-Streaming")
        self.geometry("400x350")
        self.resizable(width=False, height=False)
        self.configure(bg="#04050f")
        self.model = WebDataModel()

        self.controller = MainController(model=self.model)
        self.view = MainView(self, self.controller)
        self.view.pack(expand=tk.YES, fill=tk.BOTH)
        self.controller.view = self.view

if __name__ == "__main__":
    app = App()
    app.mainloop()