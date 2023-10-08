import tkinter as tk
from PIL import Image, ImageTk
import requests
from io import BytesIO

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
        self.buttons = []
        
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

    def setup_gif_animation(self):
        pil_image = Image.open("./icon/loading-cude.gif")
        self.num_frames = pil_image.n_frames
        new_width = 150
        new_height = 150
        self.gif_image = [ImageTk.PhotoImage(pil_image.copy().convert("RGBA").resize((new_width, new_height), Image.LANCZOS)) for frame in range(self.num_frames) if pil_image.seek(frame) is None]
        self.gif_label = tk.Label(self, image=self.gif_image[0], bg="#04050f")
        self.gif_label.grid(row=0, column=0)

    def start_gif_animation(self):
        self.update_gif_animation(0)

    def update_gif_animation(self, ind):
        try:
            frame = self.gif_image[ind]
            self.gif_label.configure(image=frame)
            self.after(125, self.update_gif_animation, (ind + 1) % self.num_frames)
        except:
            pass

    def stop_gif_animation(self):
        self.gif_label.grid_forget()

    def display_posters(self, movies):
        for btn in self.controller.buttons: 
            btn.grid_forget()
        self.controller.buttons.clear()

        for i, movie in enumerate(movies):
            title, year, img_url = movie
            try:
                img_data = self.fetch_raw_image(img_url)  # Fetch raw image data
                img = Image.open(BytesIO(img_data))
                img = img.resize((250, 375), Image.LANCZOS)
                img = ImageTk.PhotoImage(img)
                hover_img = self.create_hovered_image(img_data)  # Use raw image data to create hover image
                btn = self.create_button(title, img, hover_img, i)  # Pass both images to the create_button function
                self.buttons.append(btn)
                self.update_window_geometry(len(movies))
            except Exception as e:
                print(f"Error: {e}")

    def create_hovered_image(self, img_data):
        img = Image.open(BytesIO(img_data))
        hover_img = img.resize((int(1.025 * 250), int(1.025 * 375)), Image.LANCZOS)
        return ImageTk.PhotoImage(hover_img)
    
    def create_button(self, title, img, hover_img, i):
        entry_font = ("Segoe UI", 12)
        btn = tk.Button(self, image=img, text=title if len(title) <= 35 else title[:32] + '...',
        compound=tk.TOP, bg='#04050f', fg='white',
        activebackground='#04050f', relief=tk.FLAT, font=entry_font, activeforeground="white",
        highlightthickness=0, bd='0', width=260, height=410)
        btn.image = img
        btn.normal_image = img
        btn.hover_image = hover_img
        btn.bind('<Enter>', lambda e: e.widget.config(image=e.widget.hover_image))
        btn.bind('<Leave>', lambda e: e.widget.config(image=e.widget.normal_image))
        btn.grid(row=0, column=i + 1, rowspan=2, padx=(0, 10) if i != len(self.controller.buttons) - 1 else (0, 30))
        return btn
    
    def fetch_raw_image(self, img_url):
        if img_url.startswith('/'):
            img_url = 'https://trakt.tv/' + img_url
        response = requests.get(img_url)
        response.raise_for_status()
        return response.content
    
    def update_window_geometry(self, num_movies):
        poster_width = 268
        window_width = (poster_width * num_movies) + 430
        self.master.geometry(f'{window_width}x500')



