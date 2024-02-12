import requests
from bs4 import BeautifulSoup
import urllib.parse
from requests.exceptions import RequestException
from urllib3.exceptions import MaxRetryError


class WebDataModel:
    def __init__(self, excludes_sources):
        self.EXCLUDE_SOURCES = excludes_sources

    def get_html(self, search_query):
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

    def fetch_movie_links(self, title, year):
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
                and not any(exclude in link for exclude in self.EXCLUDE_SOURCES)
            ):
                size = size_tag.text
                file_links.append(link)
                file_sizes.append(size)

        return file_links, file_sizes

    def extract_movie_data(self, html):
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
