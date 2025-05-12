from datetime import datetime
from bs4 import BeautifulSoup
from typing import Optional
import requests
import asyncio
import os


class AutoUpdateLanguages2:
    def __init__(self):
        self.day_count = 1
        self.exp_days = 90
        self.delay = 86400  # 1 day in seconds
        self.url = "https://programminglanguages.info/languages/"

    async def start(self, output_path: Optional[str] = None):
        """Main entry point that creates output directory and starts update sequence"""
        if output_path is None:
            output_path = await self.get_default_output_path()
        
        await self.ensure_output_dir_exists(output_path)
        await self.generate_file(output_path)
        await self.start_sequence(output_path)

    async def get_default_output_path(self) -> str:
        """Get default output path in package directory"""
        proj_root_dir = os.path.abspath(os.path.dirname(__file__))
        return os.path.join(proj_root_dir, "project_output", "lang_list.txt")

    async def ensure_output_dir_exists(self, file_path: str) -> str:
        """Ensure the directory for the output file exists and return the directory path"""
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        return dir_path

    async def generate_file(self, file_path: str):
        """Generate the language list file at the specified path"""
        if os.path.isdir(file_path):
            file_path = os.path.join(file_path, "lang_list.txt")
        
        await self.ensure_output_dir_exists(file_path)
        lang_list = await self.get_lang_list()

        try:
            with open(file_path, 'w', encoding='utf-8') as lang_file:
                for ul in lang_list:
                    for li in ul:
                        text = li.string
                        if text is None or text.strip() == "":
                            continue
                        lang_file.write(text.strip() + '\n')
        except IOError as e:
            raise RuntimeError(f"Failed to write language file: {e}")

    async def start_sequence(self, output_path: str):
        """Run the periodic update sequence"""
        today, next_month = await self.get_dates()
        print(f"Today: {today}")

        while self.day_count < self.exp_days:
            remaining_days = self.exp_days - self.day_count
            print(f"Day #{self.day_count}) File Update In {remaining_days} days on {next_month}")
            
            await asyncio.sleep(self.delay)
            self.day_count += 1
        else:
            await self.generate_file(output_path)

    async def get_dates(self) -> tuple[datetime, datetime]:
        """Get current date and date for next month"""
        today = datetime.now()
        try:
            next_month = datetime(
                today.year,
                today.month + 1,
                today.day
            )
        except ValueError:
            next_month = datetime(
                today.year + 1,
                1,
                today.day
            )
        return today, next_month
    
    async def get_lang_list(self):
        """Scrape the website for programming languages list"""
        try:
            response = requests.get(self.url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html5lib')
            return soup.find_all("ul", {"class": "column-list"})
        except requests.RequestException as e:
            raise RuntimeError(f"Failed to fetch languages: {e}")


if __name__ == '__main__':
    app = AutoUpdateLanguages2()
    asyncio.run(app.start())