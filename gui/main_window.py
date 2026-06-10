# main_window.py
# This module defines the MainWindow class, which is the main interface for managing chapters and questions in the Electrolysis Quiz System. It displays a table of chapters with their numbers, titles, and question counts, and provides buttons for adding, editing, deleting chapters, managing questions, and starting quizzes. The MainWindow interacts with the database to perform CRUD operations on chapters and to launch other windows for question management and quiz taking.

from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QTableWidget,
    QTableWidgetItem,
    QPushButton,
    QHBoxLayout,
    QMessageBox
)

from database.db import (
    get_all_chapters,
    get_chapter_question_count,
    add_chapter,
    update_chapter,
    delete_chapter
)

from gui.question_window import QuestionWindow
from gui.chapter_dialog import ChapterDialog
from gui.quiz_window import QuizWindow

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle(
            "Electrolysis Quiz System"
        )

        self.resize(1000, 700)

        self.chapter_table = QTableWidget()

        self.chapter_table.setColumnCount(3)

        self.chapter_table.setHorizontalHeaderLabels(
            [
                "Chapter",
                "Title",
                "Questions"
            ]
        )

        add_button = QPushButton("Add")
        edit_button = QPushButton("Edit")
        delete_button = QPushButton("Delete")
        questions_button = QPushButton("Manage Questions")

        add_button.clicked.connect(
            self.add_chapter
        )

        edit_button.clicked.connect(
            self.edit_chapter
        )

        delete_button.clicked.connect(
            self.delete_chapter
        )

        questions_button.clicked.connect(
            self.manage_questions
        )

        button_layout = QHBoxLayout()

        button_layout.addWidget(add_button)
        button_layout.addWidget(edit_button)
        button_layout.addWidget(delete_button)
        button_layout.addWidget(questions_button) 
        quiz_button = QPushButton("Start Quiz")
        quiz_button.clicked.connect(self.start_quiz)

        button_layout.addWidget(quiz_button)  

        layout = QVBoxLayout()
        layout.addWidget(self.chapter_table)
        layout.addLayout(button_layout)

        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)

        self.load_chapters()

    def load_chapters(self):

        chapters = get_all_chapters()

        self.chapter_table.setRowCount(
            len(chapters)
        )

        for row, chapter in enumerate(chapters):

            chapter_id, number, title = chapter

            count = get_chapter_question_count(
                chapter_id
            )

            item_number = QTableWidgetItem(
                str(number)
            )

            item_title = QTableWidgetItem(
                title
            )

            item_count = QTableWidgetItem(
                str(count)
            )

            item_number.setData(
                1000,
                chapter_id
            )

            self.chapter_table.setItem(
                row,
                0,
                item_number
            )

            self.chapter_table.setItem(
                row,
                1,
                item_title
            )

            self.chapter_table.setItem(
                row,
                2,
                item_count
            )

        self.chapter_table.resizeColumnsToContents()

    def get_selected_chapter(self):

        row = self.chapter_table.currentRow()

        if row < 0:
            return None

        item = self.chapter_table.item(
            row,
            0
        )

        chapter_id = item.data(1000)

        chapter_number = int(item.text())

        title = self.chapter_table.item(
            row,
            1
        ).text()

        return (
            chapter_id,
            chapter_number,
            title
        )

    def add_chapter(self):
        dialog = ChapterDialog()

        if dialog.exec():
            add_chapter(
                dialog.chapter_number.value(),
                dialog.title_edit.text()
            )

            self.load_chapters()

    def edit_chapter(self):

        chapter = self.get_selected_chapter()

        if not chapter:
            return

        chapter_id, number, title = chapter

        dialog = ChapterDialog(
            number,
            title
        )

        if dialog.exec():

            update_chapter(
                chapter_id,
                dialog.chapter_number.value(),
                dialog.title_edit.text()
            )

            self.load_chapters()

    def delete_chapter(self):

        chapter = self.get_selected_chapter()

        if not chapter:
            return

        chapter_id, _, _ = chapter

        reply = QMessageBox.question(
            self,
            "Delete Chapter",
            "Delete selected chapter?"
        )

        if reply == QMessageBox.StandardButton.Yes:

            delete_chapter(chapter_id)

            self.load_chapters()

    def manage_questions(self):

        chapter = self.get_selected_chapter()

        if not chapter:
            return

        self.q_window = QuestionWindow()

        self.q_window.window_closed.connect(
            self.load_chapters
        )

        self.q_window.show()

    def start_quiz(self):

        chapter = self.get_selected_chapter()

        if not chapter:
            return

        chapter_id, _, _ = chapter

        self.quiz = QuizWindow(chapter_id)
        self.quiz.show()