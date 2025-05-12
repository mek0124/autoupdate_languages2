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


@pytest.mark.asyncio
async def test_get_lang_list():
    updater = AutoUpdateLanguages2()

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
    mock_response.content = fake_html

    with patch("autoupdate_languages2.core.requests.get", return_value=mock_response):
        ul_elements = await updater.get_lang_list()
        assert len(ul_elements) == 1
        assert ul_elements[0].find_all("li")[0].text == "Python"
        assert ul_elements[0].find_all("li")[1].text == "JavaScript"