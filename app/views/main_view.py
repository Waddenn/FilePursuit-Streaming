import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

class MainView(tk.Frame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        
        self.configure(bg="#04050f")
        self.setup_logo()
        self.setup_search_interface()
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=2)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        
    def setup_logo(self):
        logo_path = "./assets/icons/filepursuit.png"
        original_image = Image.open(logo_path)
        new_width = 150
        new_height = 150
        resized_image = original_image.resize((new_width, new_height), Image.LANCZOS)
        self.logo_img = ImageTk.PhotoImage(resized_image)

        self.logo_label = tk.Label(self, image=self.logo_img, bg="#04050f")
        self.logo_label.grid(row=0, column=0)

    def setup_search_interface(self):
        entry_font = ("Segoe UI", 12)
        entry_font_bold = ("Segoe UI", 12, "bold")

        self.search_entry = tk.Entry(self, font=entry_font, width=20, bg="#04050f", justify='center')
        self.search_entry.insert(0, 'Search...')
        self.search_entry.config(fg="white")
        self.search_entry.grid(row=1, column=0, sticky='n', ipady='5')
        self.search_entry.configure(insertbackground='white')
        self.search_entry.bind('<FocusIn>', self.controller.on_entry_focus_in)
        self.search_entry.bind('<FocusOut>', self.controller.on_entry_focus_out)
        self.search_entry.bind('<Return>', self.controller.main_thread)

        search_icon = Image.open("./assets/icons/glass.png")
        search_icon = search_icon.resize((20, 20), Image.LANCZOS)
        self.search_icon_photo = ImageTk.PhotoImage(search_icon)

        self.search_button = tk.Button(self, image=self.search_icon_photo, command=self.controller.main_thread, bg="#04050f", fg="#FFFFFF", relief=tk.FLAT)
        self.search_button.grid(row=1, column=0, pady=(5,0), padx=(230,0), sticky='n')  
        self.search_button.bind("<Enter>", self.controller.on_enter)
        self.search_button.bind("<Leave>", self.controller.on_leave)


