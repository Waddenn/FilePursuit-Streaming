import tkinter as tk
import threading
import subprocess
import platform


class MainController:
    def __init__(self, view=None, model=None):
        self.view = view
        self.model = model

    def on_entry_focus_in(self, event):
        if self.view.search_entry.get() == "Search...":
            self.view.search_entry.delete(0, tk.END)
            self.view.search_entry.config(fg="white", font=("Segoe UI", 12, "bold"))

    def on_entry_focus_out(self, event):
        if not self.view.search_entry.get():
            self.view.search_entry.insert(0, "Search...")
            self.view.search_entry.config(fg="gray", font=("Segoe UI", 12))

    def on_enter(self, event):
        self.view.search_button.config(width=25, height=25)

    def on_leave(self, event):
        self.view.search_button.config(width=20, height=20)

    def open_movie(self, index):
        def open_vlc():
            selected_size = self.view.size_var_list[index].get()
            movie_link = self.view.movie_links_list[index][
                self.view.size_options_list[index].index(selected_size)
            ]

            os_name = platform.system()

            if os_name == "Windows":
                vlc_path = "C:/Program Files/VideoLAN/VLC/vlc.exe"
            elif os_name == "Linux":
                vlc_path = "/usr/bin/vlc"
            elif os_name == "Darwin":
                vlc_path = "/Applications/VLC.app/Contents/MacOS/VLC"
            else:
                print("Unsupported operating system.")
                return

            subprocess.call([vlc_path, movie_link])

        vlc_thread = threading.Thread(target=open_vlc)
        vlc_thread.start()

    def main_thread(self, event=None):
        self.view.search_button.config(state=tk.DISABLED)
        self.view.setup_gif_animation()
        self.view.start_gif_animation()
        threading.Thread(target=self._long_operation).start()

    def _long_operation(self):
        try:
            query = self.view.search_entry.get()
            html = self.model.get_html(query)
            movies = self.model.extract_movie_data(html)
            print(f"Results for {movies}:")
            self.view.display_posters(movies)
            self.view.create_size_dropdowns(
                movies,
                self.view.movie_links_list,
                self.view.size_var_list,
                self.view.size_options_list,
                self.view.dropdown_menus,
            )

        finally:
            self.view.after(0, self._enable_button)
            self.view.stop_gif_animation()

    def _enable_button(self):
        self.view.search_button.config(state=tk.NORMAL)
