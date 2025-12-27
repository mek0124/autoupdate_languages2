from typing import Optional

from config import Config
from file_manager import FileManager
from schedular import Schedular
from scraper import Scraper

import asyncio


class AutoUpdateLanguages2:
    def __init__(self):
        self.config = Config
        self.file_manager = FileManager()
        self.scraper = Scraper(self.config.BASE_URL)
        self.schedular = Schedular(
            self.config.DAY_COUNT_START,
            self.config.EXPIRATION_DAYS,
            self.config.DELAY_SECONDS
        )

    async def start(self, output_path: Optional[str] = None):
        normalized_path = self.file_manager.normalize_file_path(output_path)

        await self.file_manager.ensure_output_dir_exists(normalized_path)
        await self.generate_file(normalized_path)
        await self.schedular.run_update_sequence(
            lambda: self.generate_file(normalized_path)
        )

    async def generate_file(self, file_path: str) -> None:
        lang_list = await self.get_lang_list()
        await self.file_manager.write_language_file(file_path, lang_list)

    async def get_lang_list(self) -> list:
        return await self.scraper.get_language_list()
    
    def check_scraping_permission(self) -> bool:
        return self.scraper.can_scrape()
    
    def get_update_progress(self) -> dict:
        return self.schedular.get_progress()
    

if __name__ == '__main__':
    app = AutoUpdateLanguages2()
    asyncio.run(app.start())