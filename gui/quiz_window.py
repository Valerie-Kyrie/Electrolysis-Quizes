# quiz_window.py
# This module defines the QuizWindow class, which is responsible for displaying quiz questions to the user and handling the quiz-taking process. It retrieves questions and answers from the database based on the selected chapter, presents them in a user-friendly interface, and provides feedback on the user's answers. The QuizWindow also calculates the user's score and displays it at the end of the quiz.

from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QCheckBox,
    QMessageBox
)

import random

from database.db import get_questions_by_chapter, get_answers_for_question, get_connection
from gui.answer_feedback import AnswerFeedback

class QuizWindow(QMainWindow):

    def __init__(self, chapter_id):
        super().__init__()

        self.chapter_id = chapter_id

        self.setWindowTitle("Quiz Mode")
        self.resize(700, 500)

        from database.db import get_all_questions, get_questions_by_chapter

        if chapter_id == "ALL":
            self.questions = get_all_questions()
        else:
            self.questions = get_questions_by_chapter(chapter_id)
        if not self.questions:
            QMessageBox.information(self, "No Questions", "No questions found.")
            self.close()
            return
        random.shuffle(self.questions)

        self.current_index = 0
        self.score = 0
        self.question_correct = True

        self.checkboxes = []
        

        self.question_label = QLabel()
        self.question_label.setWordWrap(True)

        self.answer_container = QWidget()
        self.answer_layout = QVBoxLayout()
        self.answer_container.setLayout(self.answer_layout)

        self.next_btn = QPushButton("Next")
        self.next_btn.clicked.connect(self.next_question)
        self.end_btn = QPushButton("End Quiz")
        self.end_btn.clicked.connect(self.end_quiz)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.question_label)

        main_layout.addWidget(self.answer_container)
        main_layout.addWidget(self.next_btn)
        main_layout.addWidget(self.end_btn)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        self.load_question()

    def load_question(self):

        self.checkboxes = []

        while self.answer_layout.count():
            item = self.answer_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.setParent(None)
                widget.deleteLater()

        self.answer_container.update()

        if self.current_index >= len(self.questions):
            self.finish_quiz()
            return

        question_id, text, page, qtype = self.questions[self.current_index]

        self.question_label.setText(text)

        answers = get_answers_for_question(question_id)
        random.shuffle(answers)

        self.checkboxes = []

        for _, answer_text, is_correct in answers:

            box = QCheckBox()
            box.setProperty("correct", is_correct)

            label = QLabel(answer_text)
            label.setWordWrap(True)

            row = QWidget()
            row_layout = QHBoxLayout()

            row_layout.setContentsMargins(0, 0, 0, 0)
            row_layout.setSpacing(5)

            row_layout.addWidget(box)
            row_layout.addWidget(label, 1)

            row.setLayout(row_layout)

            self.answer_layout.addWidget(row)

            self.checkboxes.append(box)

    def next_question(self):

        selected_any = False
        all_correct = True

        for box in self.checkboxes:

            if box.isChecked():
                selected_any = True

                if box.property("correct") != 1:
                    all_correct = False

            else:
                if box.property("correct") == 1:
                    all_correct = False

        if not selected_any:
            QMessageBox.warning(self, "Error", "Select at least one answer")
            return

        # -----------------------------
        # RESULT DIALOG (NEW UX)
        # -----------------------------
        question_id, text, page, qtype = self.questions[self.current_index]
        answers = get_answers_for_question(question_id)

        correct_answers = [a[1] for a in answers if a[2] == 1]

        # update score
        if all_correct:
            self.score += 1

        # show structured feedback window
        from gui.answer_feedback import AnswerFeedback

        dialog = AnswerFeedback(
            correct=all_correct,
            page=page,
            correct_answers=correct_answers,
            explanation=self.get_explanation(question_id)
        )

        dialog.exec()

        self.current_index += 1
        self.load_question()

    def get_explanation(self, question_id):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT explanation
            FROM questions
            WHERE id = ?
        """, (question_id,))

        row = cursor.fetchone()
        conn.close()

        if row and row[0]:
            return row[0]

        return None

    def finish_quiz(self):

        QMessageBox.information(
            self,
            "Finished",
            f"Score: {self.score} / {len(self.questions)}"
        )

        self.close()
    
    def end_quiz(self):

        answered = self.current_index  # how many completed

        if answered == 0:
            QMessageBox.information(self, "Quiz Ended", "No questions answered.")
            self.close()
            return

        QMessageBox.information(
            self,
            "Quiz Ended",
            f"You got {self.score} / {answered} correct"
        )

        self.close()