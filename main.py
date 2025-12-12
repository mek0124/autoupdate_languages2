from PySide6.QtWidgets import QApplication, QMessageBox
from dotenv import load_dotenv
from pathlib import Path

from app.app import ProgrammingLanguagesDictionary
from app.services.scraper import Scraper

import sys
import os


load_dotenv()

SCRAPE_URL = os.getenv("SCRAPE_URL", "")


def get_agreement(root_dir: Path) -> bool:
    try:
        reply = QMessageBox.question(
            None,
            "Read/Write Permissions",
            "This application requires read/write permissions to maintain its own file structure and database. Do you agree?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.Yes
        )

        if reply == QMessageBox.No:
            return False
        
        agreement_file_path = root_dir / "app" / "data" / "ua.txt"

        try:
            with open(agreement_file_path, 'w+') as updated_agreement:
                updated_agreement.write("True")

            return True
        
        except Exception as e:
            print(f"Unknown Exception Updating UA File: {e}")
            return False
        
    except Exception as e:
        print(f"Unknown Exception Retrieving User Read/Write Permissions: {e}")
        return False

def check_permissions(root_dir: Path) -> bool:
    agreement_file_path = root_dir / "app" / "data" / "ua.txt"

    try:
        return True if agreement_file_path.read_text().strip() == "True" else False
    
    except FileNotFoundError:
        data_dir = root_dir / "app" / "data"
        os.makedirs(data_dir, exist_ok=True)

        with open(agreement_file_path, 'w') as new_agreement:
            new_agreement.write("False")

        check_permissions(root_dir)
    
    except Exception as e:
        print(f"Unknown Exception Reading UA File: {e}")
        return False
    
def start(root_dir: Path, scraper: Scraper) -> None:
    app = QApplication(sys.argv)

    did_agree = check_permissions(root_dir)

    if not did_agree:
        user_agreed = get_agreement(root_dir)

        if not user_agreed:
            sys.exit(0)

    window = ProgrammingLanguagesDictionary(root_dir, scraper)
    window.show()

    sys.exit(app.exec())


if __name__ == '__main__':
    root_dir = Path(__file__).parent
    scraper = Scraper(SCRAPE_URL)

    start(root_dir, scraper)