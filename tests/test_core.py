import pytest
import os
import sys
import asyncio
from unittest.mock import patch, MagicMock, AsyncMock

# Add parent directory to path to allow importing app module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Mock the config import that app.core.py uses before importing
with patch.dict('sys.modules', {'config': MagicMock()}):
    from app.core import AutoUpdateLanguages2
    from app.file_manager import FileManager
    from app.scraper import Scraper
    from app.schedular import Schedular


class TestAutoUpdateLanguages2:
    """Test the main AutoUpdateLanguages2 class"""
    
    def test_initialization(self):
        """Test that the class initializes with all components"""
        # Mock the config module that gets imported in app.core
        with patch('app.core.config', MagicMock()):
            updater = AutoUpdateLanguages2()
            
            assert hasattr(updater, 'config')
            assert hasattr(updater, 'file_manager')
            assert hasattr(updater, 'scraper')
            assert hasattr(updater, 'schedular')
            assert isinstance(updater.file_manager, FileManager)
            assert isinstance(updater.scraper, Scraper)
            assert isinstance(updater.schedular, Schedular)

    @pytest.mark.asyncio
    async def test_start_method(self, tmp_path):
        """Test the main start method"""
        # Mock the config module
        with patch('app.core.config', MagicMock()):
            updater = AutoUpdateLanguages2()
        
        test_output_path = str(tmp_path / "output" / "lang_list.txt")
        
        # Mock the scheduler to avoid infinite loop in tests
        mock_schedule = AsyncMock()
        updater.schedular.run_update_sequence = mock_schedule
        
        with patch.object(updater.file_manager, 'ensure_output_dir_exists') as mock_ensure_dir, \
             patch.object(updater, 'generate_file') as mock_generate:
            
            mock_ensure_dir.return_value = os.path.dirname(test_output_path)
            
            await updater.start(test_output_path)
            
            mock_ensure_dir.assert_called_once()
            mock_generate.assert_called_once_with(test_output_path)
            mock_schedule.assert_called_once()

    @pytest.mark.asyncio
    async def test_start_method_no_path(self):
        """Test start method with no output path provided"""
        # Mock the config module
        with patch('app.core.config', MagicMock()):
            updater = AutoUpdateLanguages2()
        
        # Mock the scheduler to avoid infinite loop in tests
        mock_schedule = AsyncMock()
        updater.schedular.run_update_sequence = mock_schedule
        
        with patch.object(updater.file_manager, 'normalize_file_path') as mock_normalize, \
             patch.object(updater.file_manager, 'ensure_output_dir_exists') as mock_ensure_dir, \
             patch.object(updater, 'generate_file') as mock_generate:
            
            mock_normalize.return_value = "/default/path/lang_list.txt"
            mock_ensure_dir.return_value = "/default/path"
            
            await updater.start(None)
            
            mock_normalize.assert_called_once_with(None)
            mock_ensure_dir.assert_called_once_with("/default/path/lang_list.txt")
            mock_generate.assert_called_once_with("/default/path/lang_list.txt")

    @pytest.mark.asyncio
    async def test_generate_file(self, tmp_path):
        """Test file generation"""
        # Mock the config module
        with patch('app.core.config', MagicMock()):
            updater = AutoUpdateLanguages2()
        
        test_file_path = str(tmp_path / "lang_list.txt")
        
        # Create mock language data structure matching what scraper returns
        mock_li1 = MagicMock()
        mock_li1.string = 'Python'
        mock_li2 = MagicMock()
        mock_li2.string = 'JavaScript'
        mock_ul = MagicMock()
        mock_ul.find_all.return_value = [mock_li1, mock_li2]
        mock_lang_data = [mock_ul]
        
        with patch.object(updater, 'get_lang_list', return_value=mock_lang_data) as mock_get_langs, \
             patch.object(updater.file_manager, 'write_language_file') as mock_write:
            
            await updater.generate_file(test_file_path)
            
            mock_get_langs.assert_called_once()
            mock_write.assert_called_once_with(test_file_path, mock_lang_data)

    @pytest.mark.asyncio
    async def test_get_lang_list(self):
        """Test getting language list"""
        # Mock the config module
        with patch('app.core.config', MagicMock()):
            updater = AutoUpdateLanguages2()
        
        # Mock what the scraper actually returns (list of ul elements)
        mock_ul_element = MagicMock()
        mock_lang_data = [mock_ul_element]
        
        with patch.object(updater.scraper, 'get_language_list', return_value=mock_lang_data) as mock_scrape:
            result = await updater.get_lang_list()
            
            mock_scrape.assert_called_once()
            assert result == mock_lang_data

    def test_check_scraping_permission(self):
        """Test scraping permission check"""
        # Mock the config module
        with patch('app.core.config', MagicMock()):
            updater = AutoUpdateLanguages2()
        
        with patch.object(updater.scraper, 'can_scrape', return_value=True) as mock_check:
            result = updater.check_scraping_permission()
            
            mock_check.assert_called_once()
            assert result is True

    def test_get_update_progress(self):
        """Test progress reporting"""
        # Mock the config module
        with patch('app.core.config', MagicMock()):
            updater = AutoUpdateLanguages2()
        
        mock_progress = {"current_day": 1, "total_days": 90}
        
        with patch.object(updater.schedular, 'get_progress', return_value=mock_progress) as mock_progress_call:
            result = updater.get_update_progress()
            
            mock_progress_call.assert_called_once()
            assert result == mock_progress


class TestFileManager:
    """Test the FileManager class"""
    
    @pytest.mark.asyncio
    async def test_ensure_output_dir_exists(self, tmp_path):
        """Test directory creation"""
        file_manager = FileManager()
        test_file_path = str(tmp_path / "subdir" / "lang_list.txt")
        
        result = await file_manager.ensure_output_dir_exists(test_file_path)
        
        assert os.path.isdir(result)
        assert result == str(tmp_path / "subdir")
        
        # Test with existing directory
        result2 = await file_manager.ensure_output_dir_exists(test_file_path)
        assert result2 == result

    @pytest.mark.asyncio
    async def test_write_language_file(self, tmp_path):
        """Test writing language file"""
        file_manager = FileManager()
        test_file_path = str(tmp_path / "lang_list.txt")
        
        # Create mock data matching the actual structure
        mock_li1 = MagicMock()
        mock_li1.string = 'Python'
        mock_li2 = MagicMock()
        mock_li2.string = 'JavaScript'
        mock_li3 = MagicMock()
        mock_li3.string = None  # Should be skipped
        mock_li4 = MagicMock()
        mock_li4.string = '   '  # Should be skipped (whitespace only)
        
        mock_ul = MagicMock()
        mock_ul.find_all.return_value = [mock_li1, mock_li2, mock_li3, mock_li4]
        
        mock_lang_data = [mock_ul]
        
        await file_manager.write_language_file(test_file_path, mock_lang_data)
        
        assert os.path.exists(test_file_path)
        with open(test_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            assert 'Python' in content
            assert 'JavaScript' in content
            assert content.strip().endswith(',')
            # Verify empty/None items were skipped
            assert content.count(',') == 2  # Only two valid items

    @pytest.mark.asyncio
    async def test_write_language_file_with_directory(self, tmp_path):
        """Test writing language file when path is a directory"""
        file_manager = FileManager()
        
        # Create mock data
        mock_li = MagicMock()
        mock_li.string = 'Python'
        mock_ul = MagicMock()
        mock_ul.find_all.return_value = [mock_li]
        mock_lang_data = [mock_ul]
        
        await file_manager.write_language_file(str(tmp_path), mock_lang_data)
        
        expected_file = tmp_path / "lang_list.txt"
        assert expected_file.exists()
        with open(expected_file, 'r', encoding='utf-8') as f:
            assert 'Python' in f.read()

    @pytest.mark.asyncio
    async def test_write_language_file_io_error(self):
        """Test IOError handling when writing file"""
        file_manager = FileManager()
        mock_lang_data = [MagicMock()]
        
        with patch('builtins.open', side_effect=IOError("Permission denied")), \
             pytest.raises(RuntimeError, match="Failed to write language file"):
            await file_manager.write_language_file("/invalid/path/file.txt", mock_lang_data)

    def test_normalize_file_path(self):
        """Test file path normalization"""
        file_manager = FileManager()
        
        # Test with None path - mock the config import inside the method
        with patch('app.file_manager.Config') as MockConfig:
            mock_config_instance = MagicMock()
            mock_config_instance.get_default_output_path.return_value = "/default/path/lang_list.txt"
            MockConfig.get_default_output_path = mock_config_instance.get_default_output_path
            
            result = file_manager.normalize_file_path(None)
            assert result == "/default/path/lang_list.txt"
        
        # Test with provided path
        test_path = "/custom/path/file.txt"
        result = file_manager.normalize_file_path(test_path)
        assert result == test_path


class TestScraper:
    """Test the Scraper class"""
    
    def test_initialization(self):
        """Test scraper initialization"""
        base_url = "https://example.com"
        scraper = Scraper(base_url)
        assert scraper.base_url == base_url
        assert scraper.scrape_url == f"{base_url}/languages/"

    @pytest.mark.asyncio
    async def test_get_language_list_success(self):
        """Test successful language list scraping"""
        scraper = Scraper("https://programminglanguages.info")
        
        # Mock RobotFileParser and urllib.request.urlopen
        mock_robot_parser = MagicMock()
        mock_robot_parser.can_fetch.return_value = True
        
        mock_response = MagicMock()
        mock_response.read.return_value = b'<html><body><ul class="column-list"><li>Python</li></ul></body></html>'
        
        with patch('app.scraper.RobotFileParser', return_value=mock_robot_parser), \
             patch('app.scraper.urllib.request.urlopen', return_value=mock_response):
            
            result = await scraper.get_language_list()
            assert result is not None

    @pytest.mark.asyncio
    async def test_get_language_list_robots_blocked(self):
        """Test scraping when blocked by robots.txt"""
        scraper = Scraper("https://programminglanguages.info")
        
        mock_robot_parser = MagicMock()
        mock_robot_parser.can_fetch.return_value = False
        
        with patch('app.scraper.RobotFileParser', return_value=mock_robot_parser):
            with pytest.raises(PermissionError, match="Unable to scrape due to robots.txt permissions"):
                await scraper.get_language_list()

    def test_can_scrape_allowed(self):
        """Test can_scrape when allowed"""
        scraper = Scraper("https://programminglanguages.info")
        
        mock_robot_parser = MagicMock()
        mock_robot_parser.can_fetch.return_value = True
        
        with patch('app.scraper.RobotFileParser', return_value=mock_robot_parser):
            result = scraper.can_scrape()
            assert result is True

    def test_can_scrape_blocked(self):
        """Test can_scrape when blocked"""
        scraper = Scraper("https://programminglanguages.info")
        
        mock_robot_parser = MagicMock()
        mock_robot_parser.can_fetch.return_value = False
        
        with patch('app.scraper.RobotFileParser', return_value=mock_robot_parser):
            result = scraper.can_scrape()
            assert result is False


class TestSchedular:
    """Test the Schedular class"""
    
    @pytest.mark.asyncio
    async def test_run_update_sequence_completion(self):
        """Test the update sequence completes and calls callback"""
        # Use very small exp_days and delay for fast testing
        schedular = Schedular(day_count=1, exp_days=3, delay=0.001)
        mock_callback = AsyncMock()
        
        # Run sequence - should complete since day_count reaches exp_days
        await schedular.run_update_sequence(mock_callback)
        
        # Verify callback was called once when sequence completed
        assert mock_callback.called

    def test_get_progress(self):
        """Test progress reporting"""
        test_cases = [
            (1, 90, 1, 90, 89, 1.11),
            (30, 90, 30, 90, 60, 33.33),
            (90, 90, 90, 90, 0, 100.0),
            (45, 90, 45, 90, 45, 50.0),
        ]
        
        for start_day, exp_days, expected_current, expected_total, expected_remaining, expected_percent in test_cases:
            schedular = Schedular(day_count=start_day, exp_days=exp_days, delay=86400)
            progress = schedular.get_progress()
            
            assert progress["current_day"] == expected_current
            assert progress["total_days"] == expected_total
            assert progress["remaining_days"] == expected_remaining
            assert progress["progress_percentage"] == pytest.approx(expected_percent, rel=0.01)