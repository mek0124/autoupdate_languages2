"""Tests for configuration module"""
import os
import sys
from datetime import timedelta

# Add parent directory to path to allow importing app module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.config import Config


class TestConfig:
    """Test the Config class"""
    
    def test_constants(self):
        """Test that all constants are set"""
        assert Config.DAY_COUNT_START == 1
        assert Config.EXPIRATION_DAYS == 90
        assert Config.DELAY_SECONDS == 86400
        assert Config.BASE_URL == "https://programminglanguages.info"
        assert Config.DEFAULT_FILENAME == "lang_list.txt"
        assert Config.DEFAULT_OUTPUT_DIR == "data"

    def test_get_default_output_path(self):
        """Test default output path generation"""
        path = Config.get_default_output_path()
        # The path should end with the expected filename
        assert path.endswith(os.path.join("data", "lang_list.txt"))
        # The path should be absolute
        assert os.path.isabs(path)

    def test_get_update_interval(self):
        """Test update interval calculation"""
        interval = Config.get_update_interval()
        assert isinstance(interval, timedelta)
        assert interval.days == 90