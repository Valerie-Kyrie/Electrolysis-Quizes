# question_editor.py
# This module defines the QuestionEditor dialog, which is used for adding and editing quiz questions. It allows users to input the question text, select the chapter it belongs to, specify the page number, choose the question type (multiple choice or true/false), and add answers with an indication of which answer(s) are correct. The dialog interacts with the database to save the question and its associated answers.

from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QTextEdit,
    QPushButton,
    QComboBox,
    QLineEdit,
    QWidget,
    QRadioButton,
    QSpinBox,
    QMessageBox,
    QScrollArea
)

from database.db import (
    get_connection,
    get_question,
    get_answers_for_question
)


class QuestionEditor(QDialog):

    def __init__(
        self, 
        chapter_id,
        question_id=None
    ):
        super().__init__()

        self.chapter_id = chapter_id
        self.question_id = question_id
        self.setWindowTitle("Add Question")
        self.resize(700, 500)

        # -------------------------
        # QUESTION INPUT
        # -------------------------
        self.question_text = QTextEdit()

        self.page_number = QSpinBox()
        self.explanation = QTextEdit()
        self.page_number.setMinimum(1)
        self.page_number.setMaximum(9999)

        self.type_selector = QComboBox()
        self.type_selector.addItems(["mcq", "true_false"])

        self.type_selector.currentTextChanged.connect(self.on_type_change)

        # -------------------------
        # ANSWER INPUT
        # -------------------------
        self.answer_input = QLineEdit()

        self.add_answer_btn = QPushButton("Add Answer")
        self.add_answer_btn.clicked.connect(lambda checked=False: self.add_answer())

        # container for answers (IMPORTANT FIX)
        self.answer_container = QWidget()
        self.answer_layout = QVBoxLayout()
        self.answer_container.setLayout(self.answer_layout)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.answer_container)

        # -------------------------
        # SAVE BUTTON
        # -------------------------
        self.save_btn = QPushButton("Save Question")
        self.save_btn.clicked.connect(self.save_question)

        # -------------------------
        # LAYOUT
        # -------------------------
        main_layout = QVBoxLayout()

        main_layout.addWidget(QLabel("Question:"))
        main_layout.addWidget(self.question_text)

        page_layout = QHBoxLayout()
        page_layout.addWidget(QLabel("Answer Page Number:"))
        page_layout.addWidget(self.page_number)

        type_layout = QHBoxLayout()
        type_layout.addWidget(QLabel("Type:"))
        type_layout.addWidget(self.type_selector)

        answer_input_layout = QHBoxLayout()
        answer_input_layout.addWidget(self.answer_input)
        answer_input_layout.addWidget(self.add_answer_btn)

        main_layout.addLayout(page_layout)
        main_layout.addLayout(type_layout)
        
        main_layout.addWidget(QLabel("Explanation / Quote:"))
        main_layout.addWidget(self.explanation)

        main_layout.addWidget(QLabel("Answers:"))
        main_layout.addLayout(answer_input_layout)
        main_layout.addWidget(self.scroll)

        main_layout.addWidget(self.save_btn)

        self.setLayout(main_layout)

        self.on_type_change("mcq")
        if self.question_id:
            self.load_question()

    def load_question(self):

        question = get_question(
            self.question_id
        )

        if not question:
            return

        (
            _,
            _,
            question_text,
            page_number,
            question_type,
            explanation
        ) = question

        self.question_text.setText(
            question_text
        )
        self.explanation.setText(
            explanation or ""
        )   

        if page_number:
            self.page_number.setValue(
                page_number
            )

        self.type_selector.blockSignals(True)

        self.type_selector.setCurrentText(
            question_type
        )

        self.type_selector.blockSignals(False)

        # clear answer area
        while self.answer_layout.count():

            item = self.answer_layout.takeAt(0)

            if item.widget():
                item.widget().deleteLater()

        answers = get_answers_for_question(
            self.question_id
        )

        for answer in answers:

            answer_id, answer_text, is_correct = answer

            self.add_answer(
                answer_text
            )

            widget = self.answer_layout.itemAt(
                self.answer_layout.count() - 1
            ).widget()

            layout = widget.layout()

            radio = layout.itemAt(0).widget()

            radio.setChecked(
                bool(is_correct)
            )

    # -------------------------
    # TYPE SWITCH
    # -------------------------
    def on_type_change(self, qtype):

        # clear old answers
        while self.answer_layout.count():
            item = self.answer_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        if qtype == "true_false":
            self.answer_input.setDisabled(True)
            self.add_answer_btn.setDisabled(True)

            self.add_answer("True")
            self.add_answer("False")

        else:
            self.answer_input.setDisabled(False)
            self.add_answer_btn.setDisabled(False)

    # -------------------------
    # ADD ANSWER
    # -------------------------
    def add_answer(self, text=None):

        if text is None:
            text = self.answer_input.text().strip()

        if not text:
            return

        row = QWidget()

        layout = QHBoxLayout()

        radio = QRadioButton()

        answer_edit = QLineEdit()
        answer_edit.setText(text)

        delete_btn = QPushButton("Delete")

        layout.addWidget(radio)
        layout.addWidget(answer_edit)
        layout.addWidget(delete_btn)

        row.setLayout(layout)

        delete_btn.clicked.connect(
            lambda: row.deleteLater()
        )

        self.answer_layout.addWidget(row)

        self.answer_input.clear()

    # -------------------------
    # SAVE QUESTION
    # -------------------------
    def save_question(self):

        question = self.question_text.toPlainText().strip()

        if not question:
            QMessageBox.warning(self, "Error", "Question cannot be empty")
            return

        if self.answer_layout.count() < 2:
            QMessageBox.warning(self, "Error", "At least two answers required")
            return

        conn = get_connection()
        cursor = conn.cursor()

        # -------------------------
        # EDIT MODE
        # -------------------------
        if self.question_id:

            cursor.execute("""
                UPDATE questions
                SET question_text = ?,
                    page_number = ?,
                    question_type = ?,
                    explanation = ?
                WHERE id = ?
            """, (
                question,
                self.page_number.value(),
                self.type_selector.currentText(),
                self.explanation.toPlainText().strip(),
                self.question_id
            ))

            # delete old answers
            cursor.execute("""
                DELETE FROM answers
                WHERE question_id = ?
            """, (self.question_id,))

            question_id = self.question_id

        # -------------------------
        # CREATE MODE
        # -------------------------
        else:

            cursor.execute("""
                INSERT INTO questions (
                    chapter_id,
                    question_text,
                    page_number,
                    question_type,
                    explanation
                )
                VALUES (?, ?, ?, ?, ?)
            """, (
                self.chapter_id,
                question,
                self.page_number.value(),
                self.type_selector.currentText(),
                self.explanation.toPlainText().strip()
            ))

            question_id = cursor.lastrowid

        # -------------------------
        # SAVE ANSWERS (shared)
        # -------------------------
        correct_found = False

        for i in range(self.answer_layout.count()):

            widget = self.answer_layout.itemAt(i).widget()
            layout = widget.layout()

            radio = layout.itemAt(0).widget()
            answer_edit = layout.itemAt(1).widget()

            if radio.isChecked():
                correct_found = True

            cursor.execute("""
                INSERT INTO answers (
                    question_id,
                    answer_text,
                    is_correct
                )
                VALUES (?, ?, ?)
            """, (
                question_id,
                answer_edit.text(),
                1 if radio.isChecked() else 0
            ))

        if not correct_found:
            QMessageBox.warning(self, "Error", "Select at least one correct answer")
            conn.close()
            return

        conn.commit()
        conn.close()

        QMessageBox.information(self, "Saved", "Question saved successfully")
        self.accept()
