from PySide6 import QtWidgets as qtw
from pathlib import Path
from .screens.translated.landing import Ui_w_Landing
import sys


class ProgrammingLanguagesDictionary(qtw.QMainWindow, Ui_w_Landing):
    def __init__(self, root_dir: Path, scraper) -> None:
        super().__init__()

        self.root_dir = root_dir
        self.scraper = scraper

        self.setupUi(self)

        self.actionRefresh.triggered.connect(self.refresh_list)
        self.actionExit.triggered.connect(self.exit_app)

        self.populate_language_list()

    def populate_view(self, language_name: str) -> None:
        language_info = self.scraper.get_language_info(language_name)
        print(language_info)

        """
        use self.scraper class to search for the below info on the programming language

        Name: str
        Last Updated: datetime
        Created On: datetime
        Maintained By: list
        Language Icon: url
        GitHub Repo: url
        Most Commonly Used For: list
        About the language: str
        """

    def populate_language_list(self) -> None:
        lang_list = self.scraper.get_language_list()
        
        if not lang_list:
            return
        
        container = qtw.QWidget()
        vertical_layout = qtw.QVBoxLayout(container)
        
        for ul in lang_list:
            li_elements = ul.find_all('li')
            for li in li_elements:
                text = li.get_text(strip=True)
                if text:
                    button = qtw.QPushButton(text)
                    button.clicked.connect(lambda checked, lang=text: self.populate_view(lang))
                    vertical_layout.addWidget(button)
        
        vertical_layout.addStretch()
        self.scroll_language_list.setWidget(container)
        self.scroll_language_list.setWidgetResizable(True)

    def refresh_list(self) -> None:
        self.populate_language_list()

    def exit_app(self) -> None:
        sys.exit(0)