# main_menu.py
# This module defines the MainMenuWindow class, which is the main menu of the Electrolysis Quiz System. It provides buttons for starting a quiz (with chapter selection), taking a quiz with all chapters (coming soon), and managing chapters and questions. The main menu serves as the entry point for users to navigate to different parts of the application.

from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QPushButton
)

from gui.main_window import MainWindow
from gui.quiz_window import QuizWindow


class MainMenuWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Electrolysis Quiz System")
        self.resize(600, 400)

        # -----------------------
        # Buttons
        # -----------------------
        self.start_quiz_btn = QPushButton("Start Quiz (Chapter Select)")
        self.all_quiz_btn = QPushButton("All Chapters Quiz")
        self.manage_btn = QPushButton("Manage Chapters && Questions")

        # connect buttons to actions
        self.start_quiz_btn.clicked.connect(self.open_quiz)
        self.all_quiz_btn.clicked.connect(self.all_quiz_placeholder)
        self.manage_btn.clicked.connect(self.open_manage)

        # layout
        layout = QVBoxLayout()
        layout.addWidget(self.start_quiz_btn)
        layout.addWidget(self.all_quiz_btn)
        layout.addWidget(self.manage_btn)

        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)

    # -----------------------
    # BUTTON ACTIONS
    # -----------------------

    def open_quiz(self):
        from gui.chapter_select import ChapterSelectWindow

        self.chapter_select = ChapterSelectWindow()
        self.chapter_select.show()

    def all_quiz_placeholder(self):
        from gui.quiz_window import QuizWindow

        self.quiz_window = QuizWindow("ALL")
        self.quiz_window.show()

    def open_manage(self):
        self.manage_window = MainWindow()
        self.manage_window.show()