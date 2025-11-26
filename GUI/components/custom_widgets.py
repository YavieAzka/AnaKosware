# components/custom_widgets.py
from PyQt6.QtWidgets import QLineEdit, QPushButton
from PyQt6.QtGui import QEnterEvent, QFont
from PyQt6.QtCore import Qt


class PlaceholderEntry(QLineEdit):
    """QLineEdit dengan placeholder yang menghilang saat fokus"""

    def __init__(self, placeholder="", parent=None):
        super().__init__(parent)
        self.placeholder_text = placeholder
        self.setPlaceholderText(placeholder)

        # Styling dasar
        self.setStyleSheet("""
            QLineEdit {
                border: 1px solid #c9c9c9;
                border-radius: 6px;
                padding: 6px;
                font-size: 14px;
            }
        """)

    def get_value(self):
        """Mengambil value tanpa placeholder"""
        text = self.text().strip()
        if text == "" or text == self.placeholder_text:
            return ""
        return text


class StyledButton(QPushButton):
    """Button dengan efek hover (mirip Tkinter StyledButton)"""

    def __init__(self, text="", bg="#F8A80F", fg="white",
                 hover_bg="#FFB84D", fontsize=12, bold=False,
                 callback=None, parent=None):

        super().__init__(text, parent)
        self.default_bg = bg
        self.hover_bg = hover_bg

        weight = QFont.Weight.Bold if bold else QFont.Weight.Normal
        self.setFont(QFont("Arial", fontsize, weight))

        self.setCursor(Qt.CursorShape.PointingHandCursor)

        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {bg};
                color: {fg};
                border-radius: 8px;
                padding: 8px 14px;
            }}
            QPushButton:hover {{
                background-color: {hover_bg};
            }}
        """)

        if callback:
            self.clicked.connect(callback)
