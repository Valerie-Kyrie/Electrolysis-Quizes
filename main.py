# main.py
# This is the main entry point for the Electrolysis Quiz System application. It initializes the database, sets up the main menu window, and starts the PyQt application loop. The main menu allows users to navigate to different parts of the application, such as starting a quiz or managing chapters and questions.

import sys

from PyQt6.QtWidgets import QApplication

from gui.main_menu import MainMenuWindow
from database.db import initialize_database, add_wrong_flag_column


def main():
    initialize_database()
    add_wrong_flag_column()

    app = QApplication(sys.argv)

    from PyQt6.QtGui import QIcon

    app.setWindowIcon(
        QIcon("assets/icon.png")
    )

    window = MainMenuWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()