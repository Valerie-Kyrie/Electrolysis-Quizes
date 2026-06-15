# about_windows.py
# This module defines the AboutWindow class, which is a dialog window that provides information about the Electrolysis Quiz System application. It includes details about the app, the author, links to the GitHub repository and email, as well as attribution for educational content. 

from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QPushButton
)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QDesktopServices
from PyQt6.QtCore import QUrl


class AboutWindow(QDialog):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("About")
        self.resize(500, 600)

        layout = QVBoxLayout()

        # -------------------------
        # COVER IMAGE
        # -------------------------
        image = QLabel()
        pixmap = QPixmap("assets/workbook_cover.png")
        pixmap = pixmap.scaledToWidth(300, Qt.TransformationMode.SmoothTransformation)
        image.setPixmap(pixmap)
        image.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(image)

        # -------------------------
        # APP INFO
        # -------------------------
        title = QLabel("Electrolysis Quiz System")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 18px; font-weight: bold;")

        layout.addWidget(title)

        author = QLabel('Made by:<br>'
            'Valerie Renzetti'
        )
        author.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(author)

        # -------------------------
        # GITHUB LINK
        # -------------------------
        github = QLabel('GitHub Repository:<br>'
            '<a href="https://github.com/Valerie-Kyrie/Electrolysis-Quizes">'
            'https://github.com/Valerie-Kyrie/Electrolysis-Quizes</a>'
        )
        github.setOpenExternalLinks(True)
        github.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(github)

        # -------------------------
        # EMAIL LINK
        # -------------------------
        email = QLabel('Email:<br>'
            '<a href="mailto:valerie.kyrie.ren@gmail.com">'
            'valerie.kyrie.ren@gmail.com</a>'
        )
        email.setOpenExternalLinks(True)
        email.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(email)

        # -------------------------
        # ATTRIBUTION / CREDIT
        # -------------------------
        credit = QLabel()
        credit.setWordWrap(True)
        credit.setAlignment(Qt.AlignmentFlag.AlignCenter)

        credit.setText(
            'Educational content references material from:<br>'
            '<a href="https://www.milady.com/catalog/advanced-services-electrolysis-hair-removal">'
            'Milady - Advanced Electrolysis Hair Removal</a>'
        )

        credit.setOpenExternalLinks(True)
        layout.addWidget(credit)

        # -------------------------
        # CLOSE BUTTON
        # -------------------------
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.close)
        layout.addWidget(close_btn)

        self.setLayout(layout)