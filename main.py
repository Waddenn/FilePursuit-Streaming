import tkinter as tk
from app.views.main_view import MainView
from app.controllers.main_controller import MainController
from app.models.model import WebDataModel
from app.constants import (
    QUALITY_LABELS,
    SECONDARY_LABELS,
    EXCLUDE_SOURCES,
    LOGO_FILEPURSUIT_PATH,
    LOADING_CUBE_PATH,
    GLASS_BUTTON_PATH,
)


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("FilePursuit-Streaming")
        self.geometry("400x350")
        self.resizable(width=False, height=False)
        self.configure(bg="#04050f")
        self.model = WebDataModel(EXCLUDE_SOURCES)
        self.controller = MainController(model=self.model)
        self.view = MainView(
            self,
            self.controller,
            QUALITY_LABELS,
            SECONDARY_LABELS,
            LOGO_FILEPURSUIT_PATH,
            LOADING_CUBE_PATH,
            GLASS_BUTTON_PATH,
        )
        self.view.pack(expand=tk.YES, fill=tk.BOTH)
        self.controller.view = self.view


if __name__ == "__main__":
    app = App()
    app.mainloop()
