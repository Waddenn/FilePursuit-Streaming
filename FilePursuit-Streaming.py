import requests
from bs4 import BeautifulSoup
import tkinter as tk
from PIL import Image, ImageTk
from io import BytesIO
import threading
from bs4 import BeautifulSoup
import time
from urllib3.exceptions import MaxRetryError
from requests.exceptions import RequestException
import urllib.parse
import subprocess
import platform

size_var_list = []
size_options_list = []
movie_links_list = []

def main_thread(event=None):
    display_gif_animation()
    search_button.config(state=tk.DISABLED)
    threading.Thread(target=main).start()


def update_gif_animation(ind):
    global gif_label, gif_image

    try:
        frame = gif_image[ind]
        gif_label.configure(image=frame)
        window.after(125, update_gif_animation, (ind + 1) % num_frames)
    except:
        pass


def display_gif_animation():
    global gif_label, gif_image, num_frames
    pil_image = Image.open("./icon/loading-cude.gif")
    num_frames = pil_image.n_frames

    new_width = 150
    new_height = 150

    gif_image = [
        ImageTk.PhotoImage(
            pil_image.copy()
            .convert("RGBA")
            .resize((new_width, new_height), Image.LANCZOS)
        )
        for frame in range(num_frames)
        if pil_image.seek(frame) is None
    ]

    gif_label = tk.Label(window, image=gif_image[0], bg="#04050f")
    gif_label.grid(row=0, column=0)
    update_gif_animation(0)
    window.update()


def remove_gif_animation():
    global gif_label
    gif_label.grid_forget()
    logo_label.grid(row=0, column=0)


def open_movie(index):
    def open_vlc():
        selected_size = size_var_list[index].get()
        movie_link = movie_links_list[index][
            size_options_list[index].index(selected_size)
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


QUALITY_LABELS = [
    "REMUX",
    "ULTRA HD",
    "WEB-DL 1080p",
    "ULtra HDLight",
    "1080p",
    "HDLight 1080p",
    "HDLight 720p",
    "720p",
    "Blu-Ray 1080p",
    "4KLight",
    "4K",
]

SECONDARY_LABELS = ["BluRay", "VFF", "HDR", "Multi", "ENG", "x264", "HD", "VF2"]


def find_labels(text, label_list):
    return [label for label in label_list if label in text]


def get_labeled_sizes(links, sizes):
    if not links:
        return ["Not Found"]

    labeled_sizes = []
    for size, link in zip(sizes, links):
        quality_labels = find_labels(link, QUALITY_LABELS)
        secondary_labels = find_labels(link, SECONDARY_LABELS)
        all_labels = quality_labels + secondary_labels
        labeled_size = f"{size} {' '.join(all_labels)}"
        labeled_sizes.append(labeled_size)
    return labeled_sizes


def create_size_dropdowns(
    movies, movie_links_list, size_var_list, size_options_list, dropdown_menus, buttons
):
    for menu in dropdown_menus:
        menu.grid_forget()
    dropdown_menus.clear()

    for i, (title, year, _) in enumerate(movies):
        links, sizes = fetch_movie_links(title, year)
        movie_links_list.append(links)
        size_var = tk.StringVar(window)
        labeled_sizes = get_labeled_sizes(links, sizes)
        size_var.set(labeled_sizes[0])
        size_var_list.append(size_var)
        size_options_list.append(labeled_sizes)
        size_menu = create_dropdown(labeled_sizes, i, size_var)
        dropdown_menus.append(size_menu)

        if all(quality == "Not Found" for quality in labeled_sizes):
            buttons[i].config(state=tk.DISABLED)


def create_dropdown(labeled_sizes, i, size_var):
    size_menu = tk.OptionMenu(window, size_var, *labeled_sizes)
    size_menu.grid(row=2, column=i + 1, pady=(0, 20), ipadx=5, ipady=5)
    configure_dropdown_style(size_menu)
    return size_menu


def configure_dropdown_style(menu):
    menu.config(
        bg="#111c2e",
        fg="white",
        activebackground="#0f1d37",
        activeforeground="#3c597e",
        relief=tk.FLAT,
        highlightthickness=0,
        bd=0,
    )
    menu["menu"].config(
        bg="#111c2e",
        fg="white",
        activebackground="#0f1d37",
        activeforeground="#3c597e",
        bd=0,
    )


def create_hovered_image(img_data):
    img = Image.open(BytesIO(img_data))
    hover_img = img.resize((int(1.025 * 250), int(1.025 * 375)), Image.LANCZOS)
    return ImageTk.PhotoImage(hover_img)


def display_posters(movies, buttons):
    for btn in buttons:
        btn.grid_forget()
    buttons.clear()

    for i, movie in enumerate(movies):
        title, year, img_url = movie
        try:
            img_data = fetch_raw_image(img_url)
            img = Image.open(BytesIO(img_data))
            img = img.resize((250, 375), Image.LANCZOS)
            img = ImageTk.PhotoImage(img)
            hover_img = create_hovered_image(img_data)
            btn = create_button(title, img, hover_img, i, buttons)
            buttons.append(btn)
            update_window_geometry(len(movies))
        except Exception as e:
            print(f"Error: {e}")


def create_button(title, img, hover_img, i, buttons):
    btn = tk.Button(
        window,
        image=img,
        text=title if len(title) <= 35 else title[:32] + "...",
        compound=tk.TOP,
        command=lambda idx=i: open_movie(idx),
        bg="#04050f",
        fg="white",
        activebackground="#04050f",
        relief=tk.FLAT,
        font=entry_font,
        activeforeground="white",
        highlightthickness=0,
        bd="0",
        width=260,
        height=410,
    )
    btn.image = img
    btn.normal_image = img
    btn.hover_image = hover_img
    btn.bind("<Enter>", lambda e: e.widget.config(image=e.widget.hover_image))
    btn.bind("<Leave>", lambda e: e.widget.config(image=e.widget.normal_image))
    btn.grid(
        row=0,
        column=i + 1,
        rowspan=2,
        padx=(0, 10) if i != len(buttons) - 1 else (0, 30),
    )
    return btn


def fetch_raw_image(img_url):
    if img_url.startswith("/"):
        img_url = "https://trakt.tv/" + img_url
    response = requests.get(img_url)
    response.raise_for_status()
    return response.content


def update_window_geometry(num_movies):
    poster_width = 268
    window_width = (poster_width * num_movies) + 430
    window.geometry(f"{window_width}x500")


def get_html(search_query):
    try:
        url = f"https://trakt.tv/search/movies?query={search_query}"
        response = requests.get(url)
        return response.text
    except (RequestException, MaxRetryError):
        print("Network error when retrieving search page.")
        return None
    except Exception as e:
        print(
            f"An unexpected error occurred while retrieving the search page: {str(e)}"
        )
        return None


def fetch_movie_links(title, year):
    search_query = f"{title} {year}"
    search_query_encoded = urllib.parse.quote(search_query)
    url = f"https://filepursuit.com/pursuit?q={search_query_encoded}&type=video&sort=sizedesc"

    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    file_links = []
    file_sizes = []

    file_posts = soup.find_all(class_="file-post-item", limit=20)

    for post in file_posts:
        link_tag = post.find("a", onclick=True)
        onclick_attr = link_tag["onclick"]

        link_start = onclick_attr.find("('") + 2
        link_end = onclick_attr.find("')")
        link = onclick_attr[link_start:link_end]

        badge_tags = post.find_all(
            "span", class_="bg-primary text-white badge py-2 px-4"
        )

        size_tag = None
        for tag in badge_tags:
            if "GB" in tag.text or "MB" in tag.text:
                size_tag = tag
                break
        if (
            size_tag
            and not size_tag.find("a")
            and not any(
                exclude in link
                for exclude in [
                    "Sermovie",
                    "3rver",
                    "perserver",
                    "menoetius",
                    "film2serial",
                    "ftk.pw",
                    "uploadt",
                    "basnetbd",
                    "dl2.",
                    "dl.",
                    "imdb",
                    "dl8.",
                ]
            )
        ):  
            size = size_tag.text
            file_links.append(link)
            file_sizes.append(size)

    return file_links, file_sizes


def extract_movie_data(html):
    try:
        soup = BeautifulSoup(html, "html.parser")
        grid_items = soup.find_all(class_="grid-item", limit=4)

        movie_data = []

        for item in grid_items:
            title_link = item.find(class_="titles-link")
            title = title_link.get_text(strip=True)
            year = item.find(class_="year").text.strip()
            img_url = item.find(class_="real")["data-original"]
            title = title.replace(year, "").strip()
            movie_data.append((title, year, img_url))
        return movie_data
    except Exception as e:
        print(
            f"An unexpected error occurred when extracting data from the movie : {str(e)}"
        )


def main():
    start_time = time.time()
    html = get_html(search_entry.get())
    movies = extract_movie_data(html)

    global buttons, dropdown_menus
    buttons = []
    dropdown_menus = []

    display_posters(movies, buttons)

    create_size_dropdowns(
        movies,
        movie_links_list,
        size_var_list,
        size_options_list,
        dropdown_menus,
        buttons,
    )

    search_button.config(state=tk.NORMAL)
    remove_gif_animation()
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Temps d'exécution : {execution_time} secondes")


def on_entry_focus_in(event):
    if search_entry.get() == "Search...":
        search_entry.delete(0, tk.END)
        search_entry.config(fg="white", font=entry_font_bold)


def on_entry_focus_out(event):
    if not search_entry.get():
        search_entry.insert(0, "Search...")
        search_entry.config(fg="white", font=entry_font_bold)


window = tk.Tk()
window.title("FilePursuit-Streaming")
window.configure(bg="#04050f")
window.geometry("400x350")
label_font = ("Segoe UI", 12, "bold")
entry_font = ("Segoe UI", 12)
button_font = ("Segoe UI", 12, "bold")
entry_font_bold = ("Segoe UI", 12, "bold")
window.resizable(width=False, height=False)

window.grid_columnconfigure(0, weight=1)

window.grid_rowconfigure(0, weight=2)
window.grid_rowconfigure(1, weight=1)
window.grid_rowconfigure(2, weight=1)

logo_path = "./icon/filepursuit.png"
with open(logo_path, "rb") as file:
    raw_data = file.read()

original_image = Image.open(logo_path)

new_width = 150
new_height = 150

resized_image = original_image.resize((new_width, new_height), Image.LANCZOS)
logo_img = ImageTk.PhotoImage(resized_image)

logo_label = tk.Label(window, image=logo_img, bg="#04050f")
logo_label.grid(row=0, column=0)


def focus_search_entry(event):
    search_entry.focus_set()


search_entry = tk.Entry(
    window, font=entry_font, width=20, bg="#04050f", justify="center"
)
search_entry.insert(0, "Search...")
search_entry.config(fg="white")
search_entry.grid(row=1, column=0, sticky="n", ipady="5")
search_entry.configure(insertbackground="white")

search_entry.bind("<FocusIn>", on_entry_focus_in)
search_entry.bind("<FocusOut>", on_entry_focus_out)

search_icon = Image.open("./icon/glass.png")
search_icon = search_icon.resize((20, 20), Image.LANCZOS)
search_icon_photo = ImageTk.PhotoImage(search_icon)
window.search_icon_photo = search_icon_photo


def on_enter(event):
    search_button.config(width=25, height=25)


def on_leave(event):
    search_button.config(width=20, height=20)


search_button = tk.Button(
    window,
    image=search_icon_photo,
    command=main_thread,
    font=button_font,
    bg="#04050f",
    fg="#FFFFFF",
    activebackground="#04050f",
    relief=tk.FLAT,
    activeforeground="#FFFFFF",
    borderwidth=0,
)
search_button.grid(row=1, column=0, pady=(5, 0), padx=(230, 0), sticky="n")

search_button.bind("<Enter>", on_enter)
search_button.bind("<Leave>", on_leave)
window.bind("<Tab>", focus_search_entry)
search_entry.bind("<Return>", main_thread)

window.mainloop()
