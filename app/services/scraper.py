from bs4 import BeautifulSoup
from typing import List, Tuple

import urllib.request
import sqlite3 as sql


class Scraper:
    def __init__(self, root_dir, scrape_url) -> None:
        self.root_dir = root_dir
        
    def get_language_info(self, language: str):
        db_path = self.root_dir / "app" / "data" / "languages.sqlite"

        try:
            with open(db_path) as mdb:
                cur = mdb.cursor()

                all_langs = cur.execute('SELECT * FROM pldb').fetchall()

            return all_langs
        
        except Exception as e:
            raise Exception(f"Unknown Exception Reading Language Database: {e}")