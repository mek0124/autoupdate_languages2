import pytest
import asyncio
import os
from unittest.mock import patch, MagicMock
from autoupdate_languages2.core import AutoUpdateLanguages2
from pathlib import Path


@pytest.mark.asyncio
async def test_ensure_output_dir_exists(tmp_path):
    updater = AutoUpdateLanguages2()
    test_file_path = os.path.join(tmp_path, "subdir", "lang_list.txt")
    
    output_dir = await updater.ensure_output_dir_exists(test_file_path)
    
    assert os.path.isdir(output_dir)
    assert output_dir == str(tmp_path / "subdir")


@pytest.mark.asyncio
async def test_generate_file(tmp_path):
    updater = AutoUpdateLanguages2()
    mock_ul = [[MagicMock(string='Python'), MagicMock(string='JavaScript')]]
    
    test_file_path = tmp_path / "lang_list.txt"
    
    with patch.object(updater, 'get_lang_list', return_value=mock_ul):
        await updater.generate_file(str(test_file_path))
        
        assert test_file_path.exists()
        content = test_file_path.read_text()
        assert "Python" in content
        assert "JavaScript" in content


@pytest.mark.asyncio
async def test_generate_file_with_directory(tmp_path):
    updater = AutoUpdateLanguages2()
    mock_ul = [[MagicMock(string='Python'), MagicMock(string='JavaScript')]]
    
    with patch.object(updater, 'get_lang_list', return_value=mock_ul):
        await updater.generate_file(str(tmp_path))
        
        expected_file = tmp_path / "lang_list.txt"
        assert expected_file.exists()
        content = expected_file.read_text()
        assert "Python" in content
        assert "JavaScript" in content


@pytest.mark.asyncio
async def test_get_dates():
    updater = AutoUpdateLanguages2()
    today, next_month = await updater.get_dates()
    
    assert today.month in range(1, 13)
    if today.month == 12:
        assert next_month.month == 1
        assert next_month.year == today.year + 1
    else:
        assert next_month.month == today.month + 1
        assert next_month.year == today.year


# test_core.py
@pytest.mark.asyncio
async def test_get_lang_list():
    updater = AutoUpdateLanguages2()
    updater.url = "http://example.com"  # assuming this is needed for the test

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
    
    # Mock the robots.txt check to return True
    mock_robot_parser = MagicMock()
    mock_robot_parser.can_fetch.return_value = True
    
    # Mock urllib request and response
    mock_response = MagicMock()
    mock_response.read.return_value = fake_html.encode('utf-8')
    
    with patch("autoupdate_languages2.core.RobotFileParser", return_value=mock_robot_parser), \
         patch("autoupdate_languages2.core.urllib.request.urlopen", return_value=mock_response):
        
        ul_elements = await updater.get_lang_list()
        
        # Verify robots.txt check was called
        mock_robot_parser.set_url.assert_called_once_with("http://example.com/robots.txt")
        mock_robot_parser.read.assert_called_once()
        mock_robot_parser.can_fetch.assert_called_once_with("*", "http://example.com")
        
        # Verify the HTML parsing
        assert len(ul_elements) == 1
        assert ul_elements[0].find_all("li")[0].text == "Python"
        assert ul_elements[0].find_all("li")[1].text == "JavaScript"