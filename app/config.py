"""Configuration settings for AutoUpdateLanguages2"""

from datetime import timedelta

import os


class Config:
    """Configuration class for application settings"""

    # Timing settings
    DAY_COUNT_START = 1
    EXPIRATION_DAYS = 90
    DELAY_SECONDS = 86400

    # URL settings
    BASE_URL = "https://programminglanguages.info"

    # File settings
    DEFAULT_FILENAME = "lang_list.txt"
    DEFAULT_OUTPUT_DIR = "data"

    @classmethod
    def get_default_output_path(cls) -> str:
        """Get default output path in package directory"""
        proj_root_dir = os.path.abspath(os.path.dirname(__file__))
        return os.path.join(proj_root_dir, cls.DEFAULT_OUTPUT_DIR, cls.DEFAULT_FILENAME)
    
    @classmethod
    def get_update_interval(cls) -> timedelta:
        """Get the update interval as timedelta"""
        return timedelta(days=cls.EXPIRATION_DAYS)