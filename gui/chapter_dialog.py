# chapter_dialog.py
# This module defines the ChapterDialog class, which is a dialog window used for adding and editing chapters in the quiz application. It allows users to input the chapter number and title, and provides a simple interface for saving these details to the database.

from PyQt6.QtWidgets import (
    QDialog,
    QFormLayout,
    QLineEdit,
    QSpinBox,
    QPushButton,
    QVBoxLayout
)


class ChapterDialog(QDialog):
    def __init__(
        self,
        chapter_number=1,
        title=""
    ):
        super().__init__()

        self.setWindowTitle("Chapter")

        self.chapter_number = QSpinBox()
        self.chapter_number.setMinimum(1)
        self.chapter_number.setValue(chapter_number)

        self.title_edit = QLineEdit()
        self.title_edit.setText(title)

        form = QFormLayout()
        form.addRow(
            "Chapter Number",
            self.chapter_number
        )
        form.addRow(
            "Title",
            self.title_edit
        )

        save_button = QPushButton("Save")
        save_button.clicked.connect(self.accept)

        layout = QVBoxLayout()
        layout.addLayout(form)
        layout.addWidget(save_button)

        self.setLayout(layout)