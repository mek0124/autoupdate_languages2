"""Web scraping functionality for AutoUpdateLanguages2"""

from urllib.robotparser import RobotFileParser
from bs4 import BeautifulSoup

import urllib.request


class Scraper:
    """Handles web scraping operations with robots.txt compliance"""

    def __init__(self, base_url: str):
        self.base_url = base_url
        self.scrape_url = self.base_url + "/languages/"

    async def get_language_list(self) -> list:
        """Scrape the website for programming languages names and convert them to a list to return"""

        can_scrape = self.can_scrape()

        if not can_scrape:
            return PermissionError(
                "Unable to scrape due to robots.txt permissions. Find another link"
            )
        
        site = urllib.request.urlopen(self.scrape_url)
        sauce = site.read()
        soup = BeautifulSoup(sauce, "html.parser")
        return soup.find_all("ul", {"class": "column-list"})
    
    def can_scrape(self) -> bool:
        """Check if scraping is allowed by robots.txt"""

        try:
            rp = RobotFileParser()
            rp.set_url(self.base_url + "/robots.txt")
            rp.read()
            return rp.can_fetch("*", self.base_url)
        except Exception:
            return False