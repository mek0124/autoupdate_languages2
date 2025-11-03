import pytest
import os
import asyncio
from unittest.mock import patch, MagicMock, AsyncMock
from app.core import AutoUpdateLanguages2
from app.file_manager import FileManager
from app.scraper import Scraper
from app.schedular import Schedular


class TestAutoUpdateLanguages2:
    """Test the main AutoUpdateLanguages2 class"""
    
    def test_initialization(self):
        """Test that the class initializes with all components"""
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
        updater = AutoUpdateLanguages2()
        test_output_path = str(tmp_path / "output" / "lang_list.txt")
        
        with patch.object(updater.file_manager, 'ensure_output_dir_exists') as mock_ensure_dir, \
             patch.object(updater, 'generate_file') as mock_generate, \
             patch.object(updater.schedular, 'run_update_sequence') as mock_schedule:
            
            mock_ensure_dir.return_value = os.path.dirname(test_output_path)
            mock_schedule.return_value = None
            
            await updater.start(test_output_path)
            
            mock_ensure_dir.assert_called_once()
            mock_generate.assert_called_once_with(test_output_path)
            mock_schedule.assert_called_once()

    @pytest.mark.asyncio
    async def test_generate_file(self, tmp_path):
        """Test file generation"""
        updater = AutoUpdateLanguages2()
        test_file_path = str(tmp_path / "lang_list.txt")
        mock_lang_data = [[MagicMock(string='Python'), MagicMock(string='JavaScript')]]
        
        with patch.object(updater, 'get_lang_list', return_value=mock_lang_data) as mock_get_langs, \
             patch.object(updater.file_manager, 'write_language_file') as mock_write:
            
            await updater.generate_file(test_file_path)
            
            mock_get_langs.assert_called_once()
            mock_write.assert_called_once_with(test_file_path, mock_lang_data)

    @pytest.mark.asyncio
    async def test_get_lang_list(self):
        """Test getting language list"""
        updater = AutoUpdateLanguages2()
        mock_lang_data = ["Python", "JavaScript"]
        
        with patch.object(updater.scraper, 'get_language_list', return_value=mock_lang_data) as mock_scrape:
            result = await updater.get_lang_list()
            
            mock_scrape.assert_called_once()
            assert result == mock_lang_data

    def test_check_scraping_permission(self):
        """Test scraping permission check"""
        updater = AutoUpdateLanguages2()
        
        with patch.object(updater.scraper, 'can_scrape', return_value=True) as mock_check:
            result = updater.check_scraping_permission()
            
            mock_check.assert_called_once()
            assert result is True

    def test_get_update_progress(self):
        """Test progress reporting"""
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

    @pytest.mark.asyncio
    async def test_write_language_file(self, tmp_path):
        """Test writing language file"""
        file_manager = FileManager()
        test_file_path = str(tmp_path / "lang_list.txt")
        mock_lang_data = [
            [MagicMock(string='Python'), MagicMock(string='JavaScript')],
            [MagicMock(string='Java'), MagicMock(string='C++')]
        ]
        
        await file_manager.write_language_file(test_file_path, mock_lang_data)
        
        assert os.path.exists(test_file_path)
        with open(test_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            assert 'Python' in content
            assert 'JavaScript' in content
            assert 'Java' in content
            assert 'C++' in content

    @pytest.mark.asyncio
    async def test_write_language_file_with_directory(self, tmp_path):
        """Test writing language file when path is a directory"""
        file_manager = FileManager()
        mock_lang_data = [[MagicMock(string='Python')]]
        
        await file_manager.write_language_file(str(tmp_path), mock_lang_data)
        
        expected_file = tmp_path / "lang_list.txt"
        assert expected_file.exists()
        with open(expected_file, 'r', encoding='utf-8') as f:
            assert 'Python' in f.read()

    def test_normalize_file_path(self):
        """Test file path normalization"""
        file_manager = FileManager()
        
        # Test with None path
        result = file_manager.normalize_file_path(None)
        assert "lang_list.txt" in result
        
        # Test with provided path
        test_path = "/custom/path/file.txt"
        result = file_manager.normalize_file_path(test_path)
        assert result == test_path


class TestScraper:
    """Test the Scraper class"""
    
    @pytest.mark.asyncio
    async def test_get_language_list_success(self):
        """Test successful language list scraping"""
        scraper = Scraper("https://programminglanguages.info")
        fake_html = '''
        <html>
            <body>
                <ul class="column-list">
                    <li>Python</li>
                    <li>JavaScript</li>
                </ul>
            </body>
        </html>
        '''
        
        mock_response = MagicMock()
        mock_response.read.return_value = fake_html.encode('utf-8')
        
        mock_robot_parser = MagicMock()
        mock_robot_parser.can_fetch.return_value = True
        
        with patch("app.scraper.RobotFileParser", return_value=mock_robot_parser), \
             patch("app.scraper.urllib.request.urlopen", return_value=mock_response):
            
            result = await scraper.get_language_list()
            
            assert len(result) == 1
            assert result[0].find_all("li")[0].text == "Python"
            assert result[0].find_all("li")[1].text == "JavaScript"

    @pytest.mark.asyncio
    async def test_get_language_list_robots_blocked(self):
        """Test scraping when blocked by robots.txt"""
        scraper = Scraper("https://programminglanguages.info")
        
        mock_robot_parser = MagicMock()
        mock_robot_parser.can_fetch.return_value = False
        
        with patch("app.scraper.RobotFileParser", return_value=mock_robot_parser):
            with pytest.raises(PermissionError, match="Unable to scrape due to robots.txt"):
                await scraper.get_language_list()

    def test_can_scrape_allowed(self):
        """Test can_scrape when allowed"""
        scraper = Scraper("https://programminglanguages.info")
        
        mock_robot_parser = MagicMock()
        mock_robot_parser.can_fetch.return_value = True
        
        with patch("app.scraper.RobotFileParser", return_value=mock_robot_parser):
            result = scraper.can_scrape()
            assert result is True

    def test_can_scrape_blocked(self):
        """Test can_scrape when blocked"""
        scraper = Scraper("https://programminglanguages.info")
        
        mock_robot_parser = MagicMock()
        mock_robot_parser.can_fetch.return_value = False
        
        with patch("app.scraper.RobotFileParser", return_value=mock_robot_parser):
            result = scraper.can_scrape()
            assert result is False


class TestSchedular:
    """Test the Schedular class"""
    
    @pytest.mark.asyncio
    async def test_run_update_sequence(self):
        """Test the update sequence runner"""
        schedular = Schedular(day_count=1, exp_days=5, delay=0.1)  # Short delay for testing
        mock_callback = AsyncMock()
        
        # Run for a short sequence
        task = asyncio.create_task(schedular.run_update_sequence(mock_callback))
        await asyncio.sleep(0.5)  # Let it run for a bit
        task.cancel()  # Cancel since it would run indefinitely
        
        # Verify callback was called at least once (final update)
        assert mock_callback.called

    @pytest.mark.asyncio
    async def test_get_dates(self):
        """Test date calculation"""
        schedular = Schedular(1, 90, 86400)
        today, next_update = await schedular.get_dates()
        
        assert today.month in range(1, 13)
        # Basic validation that next_update is in the future
        assert next_update > today

    def test_get_progress(self):
        """Test progress reporting"""
        schedular = Schedular(day_count=30, exp_days=90, delay=86400)
        progress = schedular.get_progress()
        
        assert progress["current_day"] == 30
        assert progress["total_days"] == 90
        assert progress["remaining_days"] == 60
        assert progress["progress_percentage"] == pytest.approx(33.33, rel=0.1)