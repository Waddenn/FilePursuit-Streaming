import tkinter as tk
from app.views.main_view import MainView
from app.controllers.main_controller import MainController
from app.models.model import FileDatabase

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("FilePursuit-Streaming")
        self.geometry("400x350")
        self.resizable(width=False, height=False)
        self.configure(bg="#04050f")

        self.model = FileDatabase()  # Nouveau
        self.controller = MainController(model=self.model)  # Modification
        self.view = MainView(self, self.controller)
        self.view.pack(expand=tk.YES, fill=tk.BOTH)
        self.controller.view = self.view

        self.bind('<Tab>', self.controller.main_thread)


if __name__ == "__main__":
    app = App()
    app.mainloop()