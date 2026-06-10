# question_window.py
# This module defines the QuestionWindow class, which is a window for managing quiz questions. It allows users to select a chapter and view the questions associated with that chapter. Users can add, edit, or delete questions from this window. The QuestionWindow interacts with the database to perform these operations and updates the displayed list of questions accordingly.

from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QListWidget,
    QLabel,
    QComboBox,
    QMessageBox
)

from PyQt6.QtCore import pyqtSignal

from database.db import (
    get_all_chapters,
    get_questions_by_chapter,
    delete_question
)
from gui.question_editor import QuestionEditor


class QuestionWindow(QMainWindow):

    window_closed = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Question Manager")
        self.resize(900, 600)

        self.chapter_selector = QComboBox()
        self.chapter_selector.currentIndexChanged.connect(self.load_questions      )
        self.question_list = QListWidget()

        self.add_question_btn = QPushButton("Add Question")
        self.delete_question_btn = QPushButton("Delete Question")
        self.edit_question_btn = QPushButton("Edit Question")

        self.add_question_btn.clicked.connect(self.add_question)
        self.delete_question_btn.clicked.connect(self.delete_question)
        self.edit_question_btn.clicked.connect(self.edit_question)

        top_layout = QHBoxLayout()
        top_layout.addWidget(QLabel("Chapter:"))
        top_layout.addWidget(self.chapter_selector)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.add_question_btn)
        button_layout.addWidget(self.delete_question_btn)
        button_layout.addWidget(self.edit_question_btn)

        layout = QVBoxLayout()
        layout.addLayout(top_layout)
        layout.addWidget(self.question_list)
        layout.addLayout(button_layout)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.load_chapters()

    def load_chapters(self):

        self.chapter_selector.clear()

        chapters = get_all_chapters()

        for chapter_id, number, title in chapters:

            self.chapter_selector.addItem(
                f"{number} - {title}",
                chapter_id
            )

        self.load_questions()

    def load_questions(self):

        self.question_list.clear()

        chapter_id = self.chapter_selector.currentData()

        if not chapter_id:
            return

        from database.db import get_questions_by_chapter, get_all_questions

        if chapter_id == "ALL":
            self.questions = get_all_questions()
        else:
            self.questions = get_questions_by_chapter(chapter_id)

        for question in questions:

            question_id = question[0]
            text = question[1]

            self.question_list.addItem(
                f"{question_id}|{text}"
            )

    def add_question(self):

        chapter_id = self.chapter_selector.currentData()

        if not chapter_id:
            return

        dialog = QuestionEditor(chapter_id)

        if dialog.exec():
            self.load_questions()

    def delete_question(self):

        item = self.question_list.currentItem()

        if not item:
            return

        question_id = int(
            item.text().split("|")[0]
        )

        reply = QMessageBox.question(
            self,
            "Delete Question",
            "Delete this question?"
        )

        if reply == QMessageBox.StandardButton.Yes:

            delete_question(question_id)

            self.load_questions()

    def closeEvent(self, event):

        self.window_closed.emit()

        super().closeEvent(event)

    def edit_question(self):

        item = self.question_list.currentItem()

        if not item:
            return

        question_id = int(item.text().split("|")[0])

        chapter_id = self.chapter_selector.currentData()

        if not chapter_id:
            return

        dialog = QuestionEditor(
            chapter_id,
            question_id
        )

        if dialog.exec():
            self.load_questions()