from bs4 import BeautifulSoup
from typing import List, Tuple

import urllib.request
import wikipedia


class Scraper:
    def __init__(self, scrape_url) -> None:
        self.scrape_url = scrape_url

    def get_language_list(self) -> List:
        try:
            site = urllib.request.urlopen(self.scrape_url)
            sauce = site.read()
            soup = BeautifulSoup(sauce, "html.parser")
            return soup.find_all("ul", {"class": "column-list"})
        
        except Exception as e:
            raise Exception(f"Unknown Exception Scraping Site: {self.scrape_url}: {e}")
        
    def get_language_info(self, language: str):
        try:
            language_search = f"{language} (programming language)"
            page = wikipedia.page(language_search, auto_suggest=False)
            return page.summary
        
        except wikipedia.exceptions.PageError:
            results = wikipedia.search(language_search)
            return results
        
        except Exception as e:
            print(f"Unknown Exception Searching Wikipedia: {e}")
            return None