import tkinter as tk

class MainController:
    def __init__(self, view=None, model=None):
        self.view = view
        self.model = model

    def on_entry_focus_in(self, event):
        if self.view.search_entry.get() == 'Search...':
            self.view.search_entry.delete(0, tk.END)
            self.view.search_entry.config(fg="white", font=("Segoe UI", 12, "bold"))

    def on_entry_focus_out(self, event):
        if not self.view.search_entry.get():
            self.view.search_entry.insert(0, 'Search...')
            self.view.search_entry.config(fg="gray", font=("Segoe UI", 12))

    def on_enter(self, event):
        self.view.search_button.config(width=25, height=25)

    def on_leave(self, event):
        self.view.search_button.config(width=20, height=20)

    def main_thread(self, event=None):
        query = self.view.search_entry.get()
        results = self.model.search_files(query)
        print(f"Results for {query}:", results)
