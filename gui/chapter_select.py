# chapter_select.py
# This module defines the ChapterSelectWindow class, which is a window that allows users to select a chapter from a list of available chapters. Once a chapter is selected, the user can start a quiz for that chapter. The window retrieves chapter information from the database and displays it in a list widget.

from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QListWidget,
    QPushButton,
    QMessageBox
)

from database.db import get_all_chapters
from gui.quiz_window import QuizWindow


class ChapterSelectWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Select Chapter")
        self.resize(500, 400)

        self.chapter_list = QListWidget()
        self.start_btn = QPushButton("Start Quiz")

        self.start_btn.clicked.connect(self.start_quiz)

        layout = QVBoxLayout()
        layout.addWidget(self.chapter_list)
        layout.addWidget(self.start_btn)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.load_chapters()

    def load_chapters(self):

        self.chapter_list.clear()

        chapters = get_all_chapters()

        for chapter_id, number, title in chapters:
            self.chapter_list.addItem(
                f"{chapter_id}|Chapter {number} - {title}"
            )

    def start_quiz(self):

        item = self.chapter_list.currentItem()

        if not item:
            QMessageBox.warning(self, "Error", "Select a chapter first")
            return

        chapter_id = int(item.text().split("|")[0])

        self.quiz = QuizWindow(chapter_id)
        self.quiz.show()
        self.close()
