# components/penghuni/star_rating.py
from PyQt6.QtWidgets import QWidget, QPushButton, QHBoxLayout
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt


class StarRating(QWidget):
    """Komponen rating bintang untuk PyQt6"""

    def __init__(self, parent=None, max_stars=5, on_rating_changed=None):
        super().__init__(parent)

        self.max_stars = max_stars
        self.on_rating_changed = on_rating_changed
        self.current_rating = 0

        self.stars = []
        self.layout = QHBoxLayout()
        self.layout.setSpacing(8)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.setLayout(self.layout)

        self.create_stars()

    def create_stars(self):
        """Membuat tombol bintang"""
        for i in range(1, self.max_stars + 1):
            star_btn = QPushButton("★")
            star_btn.setFont(QFont("Arial", 22))
            star_btn.setFixedSize(32, 32)

            star_btn.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    border: none;
                    color: #CCCCCC;
                }
                QPushButton:hover {
                    color: #F7D116;
                }
            """)

            star_btn.clicked.connect(lambda _, s=i: self.set_rating(s))

            self.stars.append(star_btn)
            self.layout.addWidget(star_btn)

    def set_rating(self, value):
        """Mengatur rating ketika bintang ditekan"""
        self.current_rating = value

        for i, star in enumerate(self.stars):
            if i < value:
                star.setStyleSheet("""
                    QPushButton {
                        background-color: transparent;
                        border: none;
                        color: #F7D116;
                    }
                """)
            else:
                star.setStyleSheet("""
                    QPushButton {
                        background-color: transparent;
                        border: none;
                        color: #CCCCCC;
                    }
                """)

        if self.on_rating_changed:
            self.on_rating_changed(value)

    def reset_rating(self):
        """Reset ke nol"""
        self.set_rating(0)
