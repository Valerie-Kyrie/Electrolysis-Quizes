# answer_feedback.py
# This module defines the AnswerFeedback dialog, which is shown after a user answers a quiz question to provide feedback on whether their answer was correct, along with the correct answer(s) and any explanations.

from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QTextEdit
)


class AnswerFeedback(QDialog):

    def __init__(self, correct, page, correct_answers, explanation=None):
        super().__init__()

        self.setWindowTitle("Result")
        self.resize(500, 300)

        layout = QVBoxLayout()

        # Header
        if correct:
            title = QLabel("✔ Correct")
        else:
            title = QLabel("✘ Incorrect")

        layout.addWidget(title)

        # Page info
        layout.addWidget(QLabel(f"Page: {page}"))

        # Correct answers
        layout.addWidget(QLabel("Correct answer(s):"))

        answer_box = QTextEdit()
        answer_box.setReadOnly(True)
        answer_box.setText("\n".join(correct_answers))
        layout.addWidget(answer_box)

        # Explanation / quote (optional future field)
        if explanation:
            layout.addWidget(QLabel("Explanation:"))

            explanation_box = QTextEdit()
            explanation_box.setReadOnly(True)
            explanation_box.setText(explanation)
            layout.addWidget(explanation_box)

        # Close button
        btn = QPushButton("OK")
        btn.clicked.connect(self.accept)

        layout.addWidget(btn)

        self.setLayout(layout)