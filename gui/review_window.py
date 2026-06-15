# review_window.py
# This module defines the ReviewWindow class, which displays a list of questions that the user got wrong during a quiz. Each question is displayed with its text and the page number it is associated with. The questions are sorted by page number for easier review. The window also includes a close button to exit the review screen. This allows users to focus on the questions they struggled with and review the relevant material in their textbook.

from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QScrollArea,
    QSizePolicy
)


class ReviewWindow(QMainWindow):

    def __init__(self, wrong_questions):
        super().__init__()

        self.setWindowTitle("Questions To Review")
        self.resize(800, 600)

        self.close_btn = QPushButton("Close")
        self.close_btn.clicked.connect(self.close)

        container = QWidget()
        self.setCentralWidget(container)

        main_layout = QVBoxLayout(container)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)

        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)

        scroll_layout.setContentsMargins(10, 10, 10, 10)
        scroll_layout.setSpacing(12)

        sorted_questions = sorted(wrong_questions, key=lambda q: q[2])

        for i, (_, text, page) in enumerate(sorted_questions, start=1):

            # -------------------------
            # CARD CONTAINER (IMPORTANT FIX)
            # -------------------------
            card = QWidget()
            card_layout = QVBoxLayout(card)

            card_layout.setContentsMargins(8, 8, 8, 8)
            card_layout.setSpacing(6)

            question = QLabel(f"{i}. {text}")
            question.setWordWrap(True)

            # THIS is critical for proper height expansion
            question.setSizePolicy(
                QSizePolicy.Policy.Expanding,
                QSizePolicy.Policy.MinimumExpanding
            )

            page_label = QLabel(f"Page: {page}")
            page_label.setStyleSheet("color: gray; font-size: 11px;")

            card_layout.addWidget(question)
            card_layout.addWidget(page_label)

            # CRITICAL: force layout to compute full height correctly
            card.setSizePolicy(
                QSizePolicy.Policy.Expanding,
                QSizePolicy.Policy.Maximum
            )

            scroll_layout.addWidget(card)

        scroll.setWidget(scroll_content)

        main_layout.addWidget(scroll)
        main_layout.addWidget(self.close_btn)