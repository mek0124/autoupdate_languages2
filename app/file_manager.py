"""File management operations for AutoUpdateLanguages2"""

from typing import Optional

import os


class FileManager:
    """Handles all file system operations"""

    @staticmethod
    async def ensure_output_dir_exists(file_path: str) -> str:
        """Ensure the directory for the output file exists and return the directory path"""

        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        return dir_path
    
    @staticmethod
    async def write_language_file(file_path: str, language_data: list) -> None:
        """Write language data to the specified file path"""

        if os.path.isdir(file_path):
            from app.config import Config
            file_path = os.path.join(file_path, Config.DEFAULT_FILENAME)

        await FileManager.ensure_output_dir_exists(file_path)

        try:
            with open(file_path, 'w', encoding="utf-8") as lang_file:
                for ul in language_data:
                    for li in ul:
                        text = li.string

                        if text is None or text.strip() == "":
                            continue

                        lang_file.write(text.strip() + ', ')

        except IOError as e:
            raise RuntimeError(f"Failed to write language file: {e}")
        
    @staticmethod
    def normalize_file_path(file_path: Optional[str]) -> str:
        """Normalize file path, using default if none provided"""

        if file_path is None:
            from app.config import Config
            return Config.get_default_output_path()
        
        return file_path